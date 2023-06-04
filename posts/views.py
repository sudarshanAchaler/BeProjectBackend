from rest_framework.views import APIView
from .models import Post
from rest_framework import status
from rest_framework.response import Response
from userauth.serializers import UserSerializer
from .serializers import PostSerializer, PostCreateSerializer
from django.contrib.auth import get_user_model
from helpers.s3 import uploadPostImage
from helpers.sa import GetSentiment

User = get_user_model()

# Create your views here.
class MyProfile(APIView):
    def get(self,request,*args, **kwargs):
        user = request.user
        posts = Post.objects.filter(author=user).order_by("-created_on")
        return Response({
            "user": UserSerializer(user).data,
            "posts":PostSerializer(posts, many=True).data
        }, status=status.HTTP_200_OK)
    

class OthersProfilePage(APIView):
    def get(self, request, *args, **kwargs):
        requestor = request.user
        username = kwargs["username"]
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if not user:
            return Response({
                "error":"username does not exist"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        followers = user.followers.all()
        if requestor in followers:
            followingUser = True
        else:
            followingUser = False

        posts = Post.objects.filter(author=user).order_by("-created_on")

        return Response({
            "user": UserSerializer(user).data,
            "posts": PostSerializer(posts, many=True).data,
            "followingUser":followingUser
        },status=status.HTTP_200_OK)
    
    
class PostAPI(APIView):
    def post(self, request, *args, **kwargs):
        requestor = request.user
        media = request.data.get("image")
        body = request.data.get("body")
        serializer = PostCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if body:
            negative,positive,neutral,compound,sentiment = GetSentiment(body)
        if media:
            err,imgUrl = uploadPostImage(media,media.name)
            if err:
                return Response({
                    "error":"got an error while uploading image to s3"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            post = serializer.save(author=requestor, media=imgUrl)
        
        else:
            post = serializer.save(author=requestor,positve=positive*100,negative=negative*100, neutral=neutral*100, compound=compound)

        return Response({
            "post":PostSerializer(post).data
        },status=status.HTTP_200_OK)
    
    def get(self, request, *args, **kwargs):
        requestor = request.user
        posts = Post.objects.filter(author__followers__in=[requestor]).order_by("-created_on")
        return Response({
            "posts": PostSerializer(posts,many=True).data
        }, status=status.HTTP_200_OK)
            

        

class DeletePost(APIView):
    def delete(self,request,*args,**kwargs):
        post_id = kwargs.get("id")
        try:
            post = Post.objects.get(id=post_id)
            post.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

