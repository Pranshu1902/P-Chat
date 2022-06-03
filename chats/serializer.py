from pyrsistent import field
from rest_framework import serializers
from django.contrib.auth.models import User
from chats.models import Chat

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ["text", "sent_from", "sent_to"]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
