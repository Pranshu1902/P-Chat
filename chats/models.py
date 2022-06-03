from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Chat(models.Model):
    text = models.CharField(max_length=255)
    sent_at = models.DateTimeField(auto_now=True)
    sent_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_from', null=True, blank=True)
    sent_to = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def prettier_date(self):
        return self.sent_at.strftime("%d %b %-I:%M %p")
