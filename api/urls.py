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
    path('tags/<int:pk>/', views.TagDetails.as_view(), name='tag'),
    path('users/<int:pk>', views.UserDetails.as_view(), name='user'),
    path('profiles/<int:pk>', views.ProfileDetails.as_view(), name='profile'),
    path('news/<int:pk>', views.NewsDetails.as_view(), name='news_detail'),
    path('attachments/<int:pk>', views.AttachmentDetails.as_view(), name='attachment'),
    path('comments/<int:pk>', views.CommentDetails.as_view(), name='comment'),
]

urlpatterns = format_suffix_patterns(urlpatterns)