# Generated by Django 5.1.1 on 2024-12-05 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discord_bot', '0002_remove_livetwitch_twitch_channel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livetwitch',
            name='channel',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='livetwitch',
            name='guild',
            field=models.IntegerField(),
        ),
    ]
