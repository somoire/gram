from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.db.models import Q

import datetime as dt 

Gender = (
    ('Male', 'Male'),
    ('Female','Female'),
)
# Create your models here.
class Location(models.Model):
    location = models.CharField