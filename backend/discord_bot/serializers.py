from rest_framework import serializers
from .models import RankVoice, RankChat, LiveTwitch, RoleMessageEmoji
from twitch_bot.models import Channel

class CreateTwitchChannel(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id', 'login', 'display_name', 'background', 'icon', 'emoji_prefix']
        
class CreateLiveTwitch(serializers.ModelSerializer):
    twitch_channel= CreateTwitchChannel()
    class Meta:
        model = LiveTwitch
        fields = ['guild', 'channel', 'role', 'twitch_channel']
        
    def create(self, validated_data):
        # 先從 validated_data 中提取 items 資料
        twitch_channel_data = validated_data.pop('twitch_channel')

        # 創建訂單
        sub_data = LiveTwitch.objects.create(**validated_data)

        # 為訂單創建相關的 twitch_channel
        Channel.objects.create(sub= sub_data, **twitch_channel_data)

        return sub_data

class CreateRankChat(serializers.ModelSerializer):

    class Meta:
        model = RankChat
        fields = ['guild', 'member', 'count']
        
class CreateRankVoice(serializers.ModelSerializer):

    class Meta:
        model = RankVoice
        fields = ['guild', 'member', 'date']

class GetTwitchChannel(serializers.ModelSerializer):
    class Meta:
        model= Channel
        fields = ['id', 'login', 'display_name', 'background', 'icon', 'emoji_prefix']

class GetTwitchSub(serializers.ModelSerializer):
    twitch_channel= GetTwitchChannel(many= True)
    class Meta:
        model= LiveTwitch
        fields = ['guild', 'channel', 'role', 'twitch_channel']

class SerializerRoleMessageEmoji(serializers.ModelSerializer):
    class Meta:
        model= RoleMessageEmoji
        fields= ['guild', 'role', 'message', 'emoji']