from rest_framework import serializers

from chats.models import Chat

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ["text", "sent_from", "sent_to"]
