# Generated by Django 4.0.4 on 2022-05-30 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='sent_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
