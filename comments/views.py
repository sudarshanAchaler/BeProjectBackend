from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Comment
from .serializers import CommentSerialiser
# Create your views here.

class CommentViewSet(ModelViewSet):
    queryset= Comment.objects.all()
    serializer_class=CommentSerialiser
