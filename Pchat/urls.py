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
router.register("user", APIUserViewSet, basename="user")

# swagger
#from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='P-Chat API')

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # others
    path('admin/', admin.site.urls),
    path("about/", AboutView.as_view()),
    path("send/", CreateChat.as_view()),
    path("view/", ViewChat.as_view()),
    path("login/", UserLoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("signup/", UserSignupView.as_view()),
    path("chat/<pk>", ViewPersonalChats.as_view()),
    path("api/", include(router.urls)),
    path("", HomeView.as_view()),
    #path('login/', redirectLoggedinUser),
    #path("chat_list/", ViewSentChatList.as_view()),
    #path("api", ChatListAPI.as_view()),
    # re_path(r'^$', schema_view),
    # swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

]# + router.urls
