from rest_framework.serializers import ModelSerializer
from .models import Comment

class CommentSerialiser(ModelSerializer):
    class Meta:
        model = Comment
        fields = ["author","post","created_on","comment"]

