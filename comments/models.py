from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from posts.models import Post
# Create your models here.

User = get_user_model()

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)