"""eduhelper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import *
from rest_framework_swagger.views import get_swagger_view

from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('auth/', include('rest_auth.urls')),
    path('auth/registration/', include('rest_auth.registration.urls')),
    path('auth/get-token/', obtain_jwt_token),
    path('auth/verify-token/', verify_jwt_token),
    path('auth/refresh-token/', refresh_jwt_token),
    path('auth/get-current-user/', views.CurrentUser.as_view()),
    path('auth/get-current-user/change-photo', views.change_photo),
    path('docs/', get_swagger_view('EduHelperAPI')),
]
