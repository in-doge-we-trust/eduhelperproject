# Create your views here.
import uuid

import pyrebase
from rest_auth.registration.views import RegisterView
from rest_framework import generics
from rest_framework.decorators import *

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


class TagUnsub(generics.RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated,)

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
    path = storage.child(request.user.email).child('avatar').put(image)
    user_profile = Profile.objects.get(user=request.user.id)
    user_profile.photo_url = path.get_url()
    user_profile.save()


# TODO Check workability!!!
class NewsList(generics.ListCreateAPIView):
    queryset = News.objects.all().order_by('-created')
    serializer_class = NewsShortSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        instance = serializer.save(author=self.request.user)
        user_profile = Profile.objects.get(pk=self.request.user.id)
        for tag in self.request.data.get('add_tags'):
            if not Tag.objects.filter(name=tag).exists():
                tag_new = Tag.objects.create(name=tag)
                user_profile.tags.add(tag_new)
            instance.tags.add(Tag.objects.get(name=tag))
        user_profile.save()


class NewsDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = (IsOwnerOrAdminUserOrReadOnly,)


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
    queryset = Comment.objects.all().order_by('-created')
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
        return Comment.objects.filter(author=self.request.user).order_by('-created')


class CommentDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrAdminUserOrReadOnly,)


class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class EventDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsOwnerOrAdminUserOrReadOnly,)


class CustomRegistration(RegisterView):
    serializer_class = CustomRegistrationSerializer


class CurrentUser(generics.RetrieveAPIView,
                  generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrAdminUserOrReadOnly,)

    def get_object(self):
        return self.request.user
