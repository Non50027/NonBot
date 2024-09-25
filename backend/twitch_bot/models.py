from django.db import models

class Channel(models.Model):
    id= models.IntegerField(primary_key=True)
    name= models.CharField(max_length=50)
    display_name= models.CharField(max_length=50)
    icon= models.URLField()