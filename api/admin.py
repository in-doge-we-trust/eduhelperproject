from django.contrib import admin

# Register your models here.
from api.models import *


class ProfileAdmin(admin.ModelAdmin):
    fields = ('user', 'tags', 'photo_url')


class TagAdmin(admin.ModelAdmin):
    fields = ('name',)


class NewsAdmin(admin.ModelAdmin):
    fields = ('text', 'tags', 'author')


class AttachmentAdmin(admin.ModelAdmin):
    fields = ('url', 'label', 'owner', 'attached_to')


class CommentAdmin(admin.ModelAdmin):
    fields = ('text', 'author', 'like_counter', 'news_commented')


class EventAdmin(admin.ModelAdmin):
    fields = ('title', 'description', 'creator', 'news', 'date')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Attachment, AttachmentAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Event, EventAdmin)
