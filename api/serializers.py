from abc import ABC

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

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'like_counter', 'news_commented')


class AttachmentSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False)

    class Meta:
        model = Attachment
        fields = ('id', 'file', 'url', 'label', 'owner', 'attached_to')


class NewsSerializer(serializers.ModelSerializer):
    author = UserShortInfoSerializer(many=False, read_only=True)
    comments = CommentSerializer(many=True, required=False, read_only=True)
    attachments = AttachmentSerializer(many=True, required=False, read_only=True)
    tags = TagShortSerializer(many=True, required=False)
    file1 = serializers.FileField(required=False)
    file2 = serializers.FileField(required=False)
    file3 = serializers.FileField(required=False)
    file4 = serializers.FileField(required=False)
    file5 = serializers.FileField(required=False)

    class Meta:
        model = News
        fields = ('id', 'text', 'tags', 'author', 'comments', 'attachments',
                  'file1', 'file2', 'file3', 'file4', 'file5', 'created')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False, read_only=True)
    news = NewsSerializer(many=True)
    files = AttachmentSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'profile', 'news', 'comments', 'files')


class EventSerializer(serializers.ModelSerializer):
    creator = UserShortInfoSerializer(many=False, read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'creator', 'news', 'date')


class CustomRegistrationSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    def custom_signup(self, request, user):
        user.first_name = self.validated_data.get('first_name', '')
        user.last_name = self.validated_data.get('last_name', '')
        user.save(update_fields=['first_name', 'last_name'])

