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
    
    user_id= models.CharField(primary_key=True, max_length=50)
    user_login= models.CharField(max_length=50)
    user_name= models.CharField(max_length=50)
    channel= models.CharField(max_length=50, null=False)
    role= models.CharField(max_length=50, null=True)
    background_url= models.URLField(null=False)
    icon_url= models.URLField(null=False)
    on_live= models.BooleanField()