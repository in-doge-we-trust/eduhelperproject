from django.contrib.auth.models import User
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from api.models import Tag, Profile, News, Comment, Attachment, Event


class TagSerializer(serializers.ModelSerializer):
    subscribers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    news_marked = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Tag
        fields = ('id', 'name', 'subscribers', 'news_marked')


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Profile
        fields = ('id', 'user', 'tags', 'photo_url')


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'text', 'tags', 'author', 'comments', 'attachments', 'created')


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ('id', 'url', 'label', 'owner', 'attached_to')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'like_counter', 'news_commented')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False, read_only=True)
    news = NewsSerializer(many=True)
    files = AttachmentSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'is_active',
                  'date_joined', 'profile', 'news', 'comments', 'files')


class EventSerializer(serializers.ModelSerializer):
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

