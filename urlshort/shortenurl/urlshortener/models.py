from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class URLMapping(models.Model):
    original_url = models.URLField(max_length=200)
    shortened_url = models.CharField(max_length=200)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
