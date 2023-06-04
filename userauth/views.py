from rest_framework import permissions, generics
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import CreateUserSerializer, UserSerializer, LoginUserSerializer, UpdateUserSerializer, UserBriefSerializer
from rest_framework.views import APIView
from rest_framework import status
from helpers.s3 import uploadCoverImage, uploadProfileImage
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer
    permission_classes = [
        permissions.AllowAny,
    ]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        instance, token = AuthToken.objects.create(user)
        return Response(
            {
                "user": UserBriefSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": token,
                "expiry": instance.expiry.replace(microsecond=0).timestamp() * 1000,
            },
            status=status.HTTP_200_OK,
        )


class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = [
        permissions.AllowAny,
    ]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        instance, token = AuthToken.objects.create(user)
        return Response(
            {
                "user": UserBriefSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": token,
                "expiry": instance.expiry.replace(microsecond=0).timestamp() * 1000,
            },
            status=status.HTTP_200_OK,
        )


class AddUserImages(APIView):
    def patch(self, request, *args, **kwargs):
        user = request.user
        coverImage = request.data.get("cover")
        profileImage = request.data.get("profile")

        if not coverImage or not profileImage:
            return Response(
            {
                "error": "both profile and cover images are required",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

        error,coverUrl = uploadCoverImage(coverImage,coverImage.name)
        if error:
            return Response(
                    {"error": "got an error while uploading the cover image to s3"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        
        error,profileUrl = uploadProfileImage(profileImage,profileImage.name)
        if error:
            return Response(
                    {"error": "got an error while uploading the profile image to s3"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        
        user.profilePictureUrl = profileUrl
        user.coverPictureUrl = coverUrl
        user.save()
        
        return Response(
            {
                "user": UserBriefSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )

class UpdateProfilePicture(APIView):
    def patch(self, request, *args, **kwargs):
        user = request.user
        profileImage = request.data.get("profile")
        error,profileUrl = uploadProfileImage(profileImage,profileImage.name)
        if error:
            return Response(
                    {"error": "got an error while uploading the profile image to s3"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        user.profilePictureUrl = profileUrl
        user.save()
        return Response(
            {
                "user": UserBriefSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )

class UpdateCoverPicture(APIView):
    def patch(self, request, *args, **kwargs):
        user = request.user
        coverImage = request.data.get("cover")
        error,coverUrl = uploadCoverImage(coverImage,coverImage.name)
        if error:
            return Response(
                    {"error": "got an error while uploading the cover image to s3"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        user.coverPictureUrl = coverUrl
        user.save()
        return Response(
            {
                "user": UserBriefSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )
    
class UpdateUser(APIView):
    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = UpdateUserSerializer(user,data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated = serializer.save()
        return Response(
            {
                "user": UserSerializer(updated).data,
            },
            status=status.HTTP_200_OK,
        )
    
class FollowToggle(APIView):
    def get(self,request,*args, **kwargs):
        requestor = request.user
        username = kwargs["username"]
        user = User.objects.get(username=username)

        if requestor in user.followers.all():
            user.followers.remove(requestor)
        else:
            user.followers.add(requestor)

        return Response(
            {},
            status=status.HTTP_200_OK,
        )

class GetAllUsers(APIView):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return Response({
            "body": UserSerializer(users, many=True).data,
        },status=status.HTTP_200_OK)

# class OthersProfilePage(APIView):
#     def get(self, request, *args, **kwargs):
#         requestor = request.user
#         username = kwargs["username"]
#         user = User.objects.get(username=username)
#         # posts= Post.objects.filter(author=requestor).order_by('-created_on')
#         followers = user.followers.all()

#         if requestor in followers:
#             followingUser = True
#         else:
#             followingUser = False

#         return Response(
#             {
#                 "user": UserSerializer(user).data,
#                 # "posts": PostSerializer(posts).data,
#                 "followingUser": followingUser
#             },
#             status=status.HTTP_200_OK
#         )

        
