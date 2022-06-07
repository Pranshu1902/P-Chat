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

from django.db.models import Q 

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

class AboutView(CreateView):
    form_class = UserCreationForm
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["sender"] = user
        return context

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
        master = []
        for user in User.objects.all():
            #if user.id != self.request.user.id:
            chat = Chat.objects.filter(Q(sent_to = self.request.user, sent_from=user) | Q(sent_from = self.request.user, sent_to=user)).order_by("sent_at")
            count = chat.count()
            if count!=0:
                if len(master) == 0:
                    master.append(chat[count-1])
                else:
                    # finding the correct spot in sorted way
                    for i in range(len(master)):
                        if chat[count-1].sent_at <= master[i].sent_at:
                            master.insert(i+1, chat[count-1])
                            break
                    else:
                        master.insert(0, chat[count-1])

        return master

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
        all_chats = Chat.objects.filter(Q(sent_from=self.request.user, sent_to__id__in = receiver.all()) | Q(sent_from__id__in=receiver.all(), sent_to = self.request.user)).order_by("sent_at")
        # filter(sent | recieved)
        return all_chats

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        receiver = User.objects.filter(id = self.request.resolver_match.kwargs['pk'])
        received = Chat.objects.filter(sent_from__id__in=receiver.all(), sent_to = self.request.user)
        context["received"] = received
        context["contact"] = receiver[0]
        user = self.request.user
        context["sender"] = user
        return context
