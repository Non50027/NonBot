from django.db import models

class RankVoice(models.Model):
    guild= models.CharField(max_length=50, null=False)
    member= models.CharField(max_length=50, null=False)
    date= models.DateTimeField(null=True)

class RankChat(models.Model):
    guild= models.CharField(max_length=50, null=False)
    member= models.CharField(max_length=50, null=False)
    count= models.IntegerField()
    
class LiveTwitch(models.Model):
    guild= models.IntegerField(null=False)
    channel= models.IntegerField(null=False)
    role= models.CharField(max_length=50, null=True)

class RoleMessageEmoji(models.Model):
    guild= models.IntegerField(null=False)
    role= models.IntegerField(null=False)
    message= models.IntegerField(null=False)
    emoji= models.IntegerField(null=False)
    
