from django.http import HttpResponseRedirect
# from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.forms import ModelForm
from chats.models import Chat
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# API
from rest_framework import viewsets
from chats.serializer import *

class APIChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

class APIUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# API Swagger
#from rest_framework_swagger.views import get_swagger_view
#schema_view = get_swagger_view(title='Pastebin API')


# Create your views here.

def redirectLoggedinUser(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/home")


class AuthorizedUser(LoginRequiredMixin):
    def get_queryset(self):
        return Chat.objects.filter(sent_from=self.request.user)

class UserLoginView(LoginView):
    template_name = "login.html"
    success_url = "/send"

class UserSignupView(CreateView):
    form_class = UserCreationForm
    template_name = "signup.html"
    success_url = "/send"

    def form_valid(self, form):
        self.object = form.save()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class HomeView(CreateView):
    form_class = UserCreationForm
    template_name = "home.html"
    #success_url = "/send"

class ChatForm(ModelForm):
    class Meta:
        model = Chat
        fields = ['sent_to', 'text']

class CreateChat(LoginRequiredMixin, CreateView):
    form_class = ChatForm
    template_name = 'create_chat.html'
    success_url = '/view'

    # function to get the current user's details
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["sender"] = user
        return context

    def form_valid(self, form):
        form.save()
        self.object = form.save()
        self.object.sent_from = self.request.user
        self.object.save()
        return HttpResponseRedirect("/view")

class ViewChat(LoginRequiredMixin, ListView):
    queryset = Chat.objects.all()
    template_name = 'view_chat.html'
    context_object_name = "chats"

    # function to get the current user's details
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["sender"] = user
        return context

    def get_queryset(self):
        received = list(Chat.objects.filter(sent_to=self.request.user))
        sent = list(Chat.objects.filter(sent_from=self.request.user))
        received.extend(sent)
        return received
        # return Chat.objects.filter(sent_from=self.request.user)# | sent_to = self.request.user)

class ViewSentChatList(LoginRequiredMixin, ListView):
    queryset = Chat.objects.all()
    template_name = 'sent_chat_list.html'
    context_object_name = "chats"

    def get_queryset(self):
        return Chat.objects.filter(sent_from=self.request.user)# | sent_to = self.request.user)

class ViewPersonalChats(LoginRequiredMixin, ListView):
    queryset = Chat.objects.all()
    template_name = 'personal_chat.html'
    context_object_name = "chats"

    def get_queryset(self):
        receiver = User.objects.filter(id = self.request.resolver_match.kwargs['pk'])
        sent = list(Chat.objects.filter(sent_from=self.request.user, sent_to__id__in = receiver.all()))
        received = list(Chat.objects.filter(sent_from__id__in=receiver.all(), sent_to = self.request.user))
        sent.extend(received)
        return sent# Chat.objects.filter(sent_from=self.request.user, sent_to__id__in = receiver.all())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        receiver = User.objects.filter(id = self.request.resolver_match.kwargs['pk'])
        received = Chat.objects.filter(sent_from__id__in=receiver.all(), sent_to = self.request.user)
        context["received"] = received
        user = self.request.user
        context["sender"] = user
        return context
