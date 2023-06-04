from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    body = models.TextField(blank=False)
    created_on = models.DateTimeField(default=datetime.now)
    media = models.URLField(blank=True)
    positve = models.FloatField(default=0)
    negative = models.FloatField(default=0)
    neutral = models.FloatField(default=0)
    compound = models.FloatField(default=0)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    def __str__(self):
        return self.body