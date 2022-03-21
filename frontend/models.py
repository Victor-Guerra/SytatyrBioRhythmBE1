from re import S
from django.db import models

# Create your models here.

class Destination:
    id: int
    date: str
    title: str
    description: str
    participants: list
