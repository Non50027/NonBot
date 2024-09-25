from rest_framework import serializers
from models import RankVoice, RankChat, LiveTwitch

class CreateLiveTwitch(serializers.ModelSerializer):
    class Meta:
        model = LiveTwitch
        fields = ['user_id', 'user_login', 'user_name', 'channel', 'role', 'background_url', 'icon_url', 'on_live']

class CreateRankChat(serializers.ModelSerializer):

    class Meta:
        model = RankChat
        fields = ['guild', 'member', 'count']
        
class CreateRankVoice(serializers.ModelSerializer):

    class Meta:
        model = RankVoice
        fields = ['guild', 'member', 'date']
