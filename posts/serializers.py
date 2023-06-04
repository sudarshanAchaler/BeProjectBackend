from rest_framework import serializers
from .models import Post
import humanize
from datetime import timedelta

class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    author_profile_picture_url = serializers.SerializerMethodField()
    author_username = serializers.SerializerMethodField()
    humanizedTime = serializers.SerializerMethodField()
    userliked = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ["author","body","media", "likes", "id","author_name","author_profile_picture_url","author_username","humanizedTime","userliked", "positve","negative","neutral","compound"]

    def get_author_name(self,obj):
        return obj.author.first_name + " " + obj.author.last_name
    
    def get_author_profile_picture_url(self,obj):
        return obj.author.profilePictureUrl
    
    def get_author_username(self,obj):
        return obj.author.username
    
    def get_humanizedTime(self,obj):
        time = obj.created_on 
        return humanize.naturaltime(time.replace(tzinfo=None))
    
    def get_userliked(self,obj):
        return True
    
class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["body"]