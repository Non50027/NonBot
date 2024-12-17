from django.db import models
from discord_bot.models import LiveTwitch

class Channel(models.Model):
    id= models.CharField(max_length= 20, primary_key=True)
    login= models.CharField(max_length=50)
    display_name= models.CharField(max_length=50, null= True)
    background= models.URLField(null=True)
    icon= models.URLField()
    emoji_prefix= models.CharField(max_length= 10, null= True)
    sub= models.ForeignKey(LiveTwitch, related_name= 'twitch_channel', on_delete= models.CASCADE, null= True)