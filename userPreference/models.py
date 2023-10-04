from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class userPreference(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    currency = models.CharField(max_length=255,blank=True,null=True)

    def __str__(self):
        return self.user.username
    
class Categories(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name