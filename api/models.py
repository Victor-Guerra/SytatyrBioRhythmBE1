from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    
    
class Event(models.Model):
    date_and_time = models.DateTimeField(("date_and_time"), auto_now=True)
# Create your models here.
