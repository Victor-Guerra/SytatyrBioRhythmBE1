from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    
    
class Event(models.Model):
    date_and_time = models.DateTimeField(("date_and_time"), auto_now=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ForeignKey(User)
# Create your models here.