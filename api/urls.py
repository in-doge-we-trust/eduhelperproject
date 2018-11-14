from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from api import views

urlpatterns = [
    path('tags/', views.TagList.as_view()),
    path('users/', views.UserList.as_view()),
    path('profiles/', views.ProfileList.as_view()),
    path('news/', views.NewsList.as_view()),
    path('attachments/', views.AttachmentList.as_view()),
    path('comments/', views.CommentList.as_view()),
    path('tags/<int:pk>/', views.TagDetails.as_view()),
    path('users/<int:pk>', views.UserDetails.as_view()),
    path('profiles/<int:pk>', views.ProfileDetails.as_view()),
    path('news/<int:pk>', views.NewsDetails.as_view()),
    path('attachments/<int:pk>', views.AttachmentDetails.as_view()),
    path('comments/<int:pk>', views.CommentDetails.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)