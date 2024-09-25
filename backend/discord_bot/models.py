from django.db import models

class Role(models.Model):
    id= models.IntegerField(primary_key=True)
    
class Member(models.Model):
    id= models.IntegerField(primary_key=True)
    role= models.ForeignKey(Role, related_name= 'member', on_delete= models.CASCADE, null=True)
    
class Channel(models.Model):
    id= models.IntegerField(primary_key=True)
    
class Emoji(models.Model):
    id= models.IntegerField(primary_key=True)

class Guild(models.Model):
    id= models.IntegerField(primary_key=True)
    member= models.ForeignKey(Member, related_name= 'guild', on_delete= models.CASCADE, null=True)
    channel= models.ForeignKey(Channel, related_name= 'guild', on_delete= models.CASCADE, null=True)
    emoji= models.ForeignKey(Emoji, related_name= 'guild', on_delete= models.CASCADE, null=True)
    role= models.ForeignKey(Role, related_name= 'guild', on_delete= models.CASCADE, null=True)
    
class Rank(models.Model):
    class Type(models.TextChoices):
        CHAT= 'chat'
        VOICE= 'voice'
        
    guild= models.ForeignKey(Guild, related_name= 'rank', on_delete= models.CASCADE)
    member= models.ForeignKey(Member, related_name= 'rank', on_delete= models.CASCADE)
    type= models.CharField(max_length=50, choices= Type.choices)
    day= models.IntegerField(default=0)
    value= models.CharField(max_length=20)
    
class Live(models.Model):
    class Media(models.TextChoices):
        TWITCH= 'twitch'
        YOUTUBE= 'youtube'
    
    id= models.CharField(primary_key=True, max_length=50)
    channel= models.ForeignKey(Channel, related_name= 'live', on_delete= models.CASCADE)
    role= models.ForeignKey(Role, related_name= 'live', on_delete= models.CASCADE)
    media= models.CharField(max_length=50, choices= Media.choices, default= Media.TWITCH)
    name= models.CharField(max_length=50)
    display_name= models.CharField(max_length=50)
    icon= models.URLField()
    on_live= models.BooleanField()