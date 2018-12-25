from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from api import views

urlpatterns = [
    path('tags/', views.TagList.as_view(), name='tags'),
    path('users/', views.UserList.as_view(), name='users'),
    path('profiles/', views.ProfileList.as_view(), name='profiles'),
    path('news/', views.NewsList.as_view(), name='news'),
    path('attachments/', views.AttachmentList.as_view(), name='attachments'),
    path('comments/', views.CommentList.as_view(), name='comments'),
    path('events/', views.EventList.as_view(), name='events'),
    path('tags/<int:pk>', views.TagDetails.as_view(), name='tag'),
    path('tags/<int:pk>/sub', views.TagSub.as_view(), name='subscribe'),
    path('tags/<str:name>/sub-name', views.TagSubByName.as_view(), name='subscribe'),
    path('tags/<int:pk>/unsub', views.TagUnsub.as_view(), name='subscribe'),
    path('tags/<str:name>/unsub-name', views.TagUnsubByName.as_view(), name='subscribe'),
    path('users/<int:pk>', views.UserDetails.as_view(), name='user'),
    path('profiles/<int:pk>', views.ProfileDetails.as_view(), name='profile'),
    path('news/<int:pk>', views.NewsDetails.as_view(), name='news_detail'),
    path('news/<int:pk>/add-comment', views.CommentAdd.as_view(), name='add_comment'),
    path('feed', views.Feed.as_view(), name='feed'),
    path('find/', views.NewsListByTags.as_view(), name='find'),
    path('attachments/<int:pk>', views.AttachmentDetails.as_view(), name='attachment'),
    path('comments/<int:pk>', views.CommentDetails.as_view(), name='comment'),
    path('comments/my', views.UserComments.as_view(), name='comments_my'),
    path('events/<int:pk>', views.EventDetails.as_view(), name='event'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
