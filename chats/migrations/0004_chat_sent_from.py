# Generated by Django 4.0.2 on 2022-05-31 07:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chats', '0003_remove_chat_sent_from_remove_chat_sent_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='sent_from',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sent_from', to=settings.AUTH_USER_MODEL),
        ),
    ]