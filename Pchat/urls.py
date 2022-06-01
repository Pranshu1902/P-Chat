"""Pchat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include, re_path
from django.contrib.auth.views import LogoutView
from chats.views import *

from chats.apiviews import *

from rest_framework.routers import SimpleRouter

router = SimpleRouter(trailing_slash=True)

router.register("api", ChatViewSet, basename="chats")
router.register("chats", APIChatViewSet, basename="chats")

# swagger
#from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='P-Chat API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path("send/", CreateChat.as_view()),
    path("view/", ViewChat.as_view()),
    path("login/", UserLoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("signup/", UserSignupView.as_view()),
    path("chat_list/", ViewSentChatList.as_view()),
    path("chat/<pk>", ViewPersonalChats.as_view()),
    #path("api", ChatListAPI.as_view()),
    path("mainapi/", include(router.urls)),
    re_path(r'^$', schema_view),
]# + router.urls
