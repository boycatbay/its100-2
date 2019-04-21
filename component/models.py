import datetime
from django.db import models
from django.utils import timezone



    
class assignment(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    score = models.CharField(max_length=3)
    materialeasy = models.CharField(max_length=500)
    materialmed = models.CharField(max_length=500)
    materialhard = models.CharField(max_length=500)
