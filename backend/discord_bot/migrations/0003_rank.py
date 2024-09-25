# Generated by Django 5.1.1 on 2024-09-22 16:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discord_bot', '0002_channel_emoji_live_role_delete_item_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('chat', 'Chat'), ('voice', 'Voice')], max_length=50)),
                ('day', models.IntegerField(default=0)),
                ('value', models.CharField(max_length=20)),
                ('guild', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rank', to='discord_bot.guild')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rank', to='discord_bot.member')),
            ],
        ),
    ]
