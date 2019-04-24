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

class shardCal(models.Model):
    email = models.CharField(max_length=50)
    

class assignmentRation(models.Model):
    easy = models.CharField(max_length=1)
    med = models.CharField(max_length=1)
    hard = models.CharField(max_length=1)
    