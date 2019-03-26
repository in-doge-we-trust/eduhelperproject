# Create your views here.
import uuid

import pyrebase
from allauth.account.models import EmailAddress
from rest_auth.registration.views import RegisterView
from rest_framework import generics
from rest_framework.decorators import *
from rest_framework.response import Response

from api.permissions import *
from api.serializers import *
from eduhelper.settings import API_KEY, MESSAGING_SENDER_ID

config = {
    'apiKey': API_KEY,
    'authDomain': 'eduhelperproject-a1052.firebaseapp.com',
    'databaseURL': 'https://eduhelperproject-a1052.firebaseio.com',
    'projectId': 'eduhelperproject-a1052',
    'storageBucket': 'eduhelperproject-a1052.appspot.com',
    'messagingSenderId': MESSAGING_SENDER_ID,
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()


class TagList(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class TagDetails(generics.RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class TagSub(generics.RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=self.request.user.id)
        profile.tags.add(self.get_object())
        profile.save()
        return super().get(request, *args, **kwargs)


class TagSubByName(generics.RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'name'

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=self.request.user.id)
        profile.tags.add(self.get_object())
        profile.save()
        return super().get(request, *args, **kwargs)


class TagUnsub(generics.RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=self.request.user.id)
        profile.tags.remove(self.get_object())
        profile.save()
        return super().get(request, *args, **kwargs)


class TagUnsubByName(generics.RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'name'

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=self.request.user.id)
        profile.tags.remove(self.get_object())
        profile.save()
        return super().get(request, *args, **kwargs)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class UserDetails(generics.RetrieveAPIView,):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrAdminUserOrReadOnly,)


class ProfileList(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ProfileDetails(generics.RetrieveAPIView, generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsOwnerOrAdminUserOrReadOnly,)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_photo(request):
    image = request.FILES['image']
    uploaded = storage.child(request.user.email).child('avatar').put(image)
    user_profile = Profile.objects.get(user=request.user.id)
    user_profile.photo_url = storage.child(request.user.email).child('avatar').get_url(uploaded['downloadTokens'])
    user_profile.save()
    return Response({"message": "User profile photo successfully changed."})


class NewsList(generics.ListCreateAPIView):
    serializer_class = NewsShortSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        instance = serializer.save(author=self.request.user)
        user_profile = Profile.objects.get(user=self.request.user.id)
        for tag in self.request.data.get('add_tags'):
            print(tag)
            if Tag.objects.filter(name=tag).exists():
                print("Tag %s already exists.".format(tag))
                user_profile.tags.add(Tag.objects.get(name=tag))
            else:
                tag_new = Tag.objects.create(name=tag)
                print("Tag %s created.".format(tag_new.name))
                user_profile.tags.add(tag_new)
                print("Tag %s added to user's profile.".format(tag_new.name))
            instance.tags.add(Tag.objects.get(name=tag))

    def get_queryset(self):
        start = self.request.GET.get('start', default=0)
        end = self.request.GET.get('end', default=0)
        if int(start) > 0 and int(end) != 0:
            return News.objects.filter(pk__lte=end).filter(pk__gte=start).order_by('-created')
        else:
            return News.objects.all().order_by('-created')


class NewsDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = (IsOwnerOrAdminUserOrReadOnly,)


class NewsListByTags(generics.ListAPIView):
    serializer_class = NewsShortSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        tag_names = self.request.query_params.getlist('tag')
        tag_names_format = []
        for tag in tag_names:
            tag_names_format.append('#' + tag)
        query = News.objects.filter(tags__name__in=tag_names_format).distinct()
        for tag in tag_names_format:
            query = query.filter(tags__name__contains=tag).distinct()
        return query.order_by('-created')


class Feed(generics.ListAPIView):
    serializer_class = NewsShortSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user)
        return News.objects.filter(tags__in=profile.tags.all()).distinct().order_by('-created')


class AttachmentList(generics.ListCreateAPIView):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        path = storage.child(self.request.user.email)\
            .child(self.request.POST.get('label') + 's')\
            .child(uuid.uuid4())
        path.put(self.request.POST.get('file'))
        serializer.save(owner=self.request.user, url=path.get_url())


class AttachmentDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = (permissions.IsAdminUser,)


class CommentList(generics.ListAPIView):
    queryset = Comment.objects.all().order_by('-id')
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated,)


class CommentAdd(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author=User.objects.get(pk=self.request.user.id),
                        news_commented=News.objects.get(pk=self.kwargs.get('pk')))


class UserComments(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user).order_by('-id')


class CommentDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrAdminUserOrReadOnly,)


# class EventList(generics.ListCreateAPIView):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#
#     def perform_create(self, serializer):
#         serializer.save(creator=self.request.user)
#
#
# class EventDetails(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer
#     permission_classes = (IsOwnerOrAdminUserOrReadOnly,)
#
#
# class EventAdd(generics.ListCreateAPIView):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer
#     permission_classes = (IsOwnerOrAdminUserOrReadOnly,)
#
#     def perform_create(self, serializer):
#         serializer.save(news=self.kwargs.get('id'),
#                         creator=self.request.user.id)


class CustomRegistration(RegisterView):
    serializer_class = CustomRegistrationSerializer


class CurrentUser(generics.RetrieveAPIView,
                  generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrAdminUserOrReadOnly,)

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        if request.data['email'] != self.request.user.email:
            EmailAddress.objects.create(email=request.data['email'], user=self.request.user, primary=True)
            EmailAddress.objects.filter(user=self.request.user).exclude(email=request.data['email']).delete()
        return super().update(request, *args, **kwargs)


