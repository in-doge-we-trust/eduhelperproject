from django.contrib.auth.models import User
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from api.models import Tag, Profile, News, Comment, Attachment, Event


class TagSerializer(serializers.ModelSerializer):
    subscribers = serializers.PrimaryKeyRelatedField(many=True, read_only=True, allow_null=True)
    news_marked = serializers.PrimaryKeyRelatedField(many=True, read_only=True, allow_null=True)

    class Meta:
        model = Tag
        fields = ('id', 'name', 'subscribers', 'news_marked')


class TagShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    photo_file = serializers.ImageField(required=False)
    tags = TagShortSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'user', 'tags', 'photo_url', 'photo_file')


class UserShortInfoSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'profile')


class CommentSerializer(serializers.ModelSerializer):
    author = UserShortInfoSerializer(many=False, read_only=True)
    like_counter = serializers.IntegerField(read_only=True)
    news_commented = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'created', 'like_counter', 'news_commented')


class AttachmentSerializer(serializers.ModelSerializer):
    file = serializers.FileField()
    url = serializers.URLField(read_only=True)
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    attached_to = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Attachment
        fields = ('id', 'file', 'url', 'label', 'owner', 'attached_to', 'uploaded')


class EventSerializer(serializers.ModelSerializer):
    creator = UserShortInfoSerializer(many=False, read_only=True)
    date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'creator', 'news', 'date')


class EventShortSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'date')


class NewsSerializer(serializers.ModelSerializer):
    author = UserShortInfoSerializer(many=False, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    attachments = AttachmentSerializer(many=True, read_only=True)
    tags = TagShortSerializer(many=True, read_only=True)
    event = EventShortSerializer(read_only=True, many=False)

    class Meta:
        model = News
        fields = ('id', 'text', 'tags', 'author', 'event', 'comments', 'attachments', 'created')


class NewsShortSerializer(serializers.ModelSerializer):
    author = UserShortInfoSerializer(many=False, read_only=True)
    attachments = AttachmentSerializer(many=True, required=False, read_only=True)
    tags = TagShortSerializer(many=True, required=False, read_only=True)
    # uploads = serializers.ListField(
    #     child=serializers.FileField(max_length=20000, required=False, allow_empty_file=True),
    #     required=False, write_only=True
    # )
    add_tags = serializers.ListField(
        child=serializers.CharField(max_length=50), write_only=True,
    )
    event = EventShortSerializer(read_only=True, many=False)

    class Meta:
        model = News
        fields = ('id', 'text', 'tags', 'event', 'add_tags', 'author', 'attachments', 'created')

    def create(self, validated_data):
        validated_data.pop('add_tags', None)
        return super().create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False, read_only=True)
    news = NewsSerializer(many=True, read_only=True)
    files = AttachmentSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'profile', 'news', 'comments', 'files')


class CustomRegistrationSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    def custom_signup(self, request, user):
        user.first_name = self.validated_data.get('first_name', '')
        user.last_name = self.validated_data.get('last_name', '')
        user.save(update_fields=['first_name', 'last_name'])
