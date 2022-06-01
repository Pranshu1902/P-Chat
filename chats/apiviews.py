from django.views import View
from django.http.response import JsonResponse
from rest_framework.serializers import ModelSerializer
from chats.models import Chat
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]

class TaskSerializer(ModelSerializer):

    # user = UserSerializer(read_only=True)

    class Meta:
        model = Chat
        fields = ["id", "text", "sent_from", "sent_to"]


class ChatViewSet(LoginRequiredMixin, ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = TaskSerializer

    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Chat.objects.filter(sent_from=self.request.user)

    #def perform_create(self, serializer):
    #    serializer.save(user=self.request.user)

class ChatListAPI(View):

    def get(self, request):
        chats = Chat.objects.all()
        data = []
        for chat in chats:
            data.append({"id": chat.id, "Chat": chat.text, "sent_from": chat.sent_from, "sent_to": chat.sent_to.username})
        return JsonResponse({"Pchat": data})
