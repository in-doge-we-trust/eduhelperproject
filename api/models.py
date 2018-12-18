from django.contrib.auth.models import User
from django.db import models


# Create your models here.

ATTACHMENT_TYPES = (('image', 'image'), ('video', 'video'), ('link', 'link'), ('file', 'file'))


class Tag(models.Model):
    name = models.CharField(max_length=50, blank=False, default='')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    tags = models.ManyToManyField(Tag, related_name='subscribers', blank=True)
    photo_url = models.URLField(blank=True)


class News(models.Model):
    text = models.TextField(blank=False, default='')
    tags = models.ManyToManyField(Tag, related_name='news_marked', blank=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, related_name='news')
    created = models.DateTimeField(auto_now_add=True)


class Attachment(models.Model):
    url = models.URLField()
    owner = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, related_name='files')
    attached_to = models.ForeignKey(News, on_delete=models.CASCADE, blank=True, null=True, related_name='attachments')
    label = models.CharField(max_length=50, choices=ATTACHMENT_TYPES, default='link')
    uploaded = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    text = models.TextField(blank=False, default='')
    author = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, related_name='comments')
    like_counter = models.BigIntegerField(default=0)
    news_commented = models.ForeignKey(News, on_delete=models.CASCADE, null=True, blank=False, related_name='comments')


class Event(models.Model):
    title = models.TextField(blank=False, default='')
    description = models.TextField(blank=True, default='')
    creator = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=False, related_name='events_created')
    news = models.ForeignKey(News, on_delete=models.CASCADE, null=True, blank=True, related_name='event')
    date = models.DateTimeField()
