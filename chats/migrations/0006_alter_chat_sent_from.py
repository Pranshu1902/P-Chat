# Generated by Django 4.0.2 on 2022-05-31 10:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chats', '0005_alter_chat_sent_from'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='sent_from',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
