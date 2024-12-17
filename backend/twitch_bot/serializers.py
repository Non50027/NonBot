from rest_framework import serializers
from .models import Channel
from twitch_bot.models import Channel

class GetTwitchChannel(serializers.ModelSerializer):
    class Meta:
        model= Channel
        fields = ['id', 'login', 'display_name', 'background', 'icon', 'emoji_prefix']
