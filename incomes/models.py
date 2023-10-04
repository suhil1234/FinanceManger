from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from userPreference.models import Categories

# Create your models here.

class Income(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    category = models.ForeignKey(Categories,on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)


