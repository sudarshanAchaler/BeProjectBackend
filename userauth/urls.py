from django.urls import path
from .views import RegistrationAPI, LoginAPI, AddUserImages, UpdateCoverPicture, UpdateProfilePicture, UpdateUser, FollowToggle
from posts.views import MyProfile, OthersProfilePage

urlpatterns = [
    path("register/", RegistrationAPI.as_view()),
    path("login/", LoginAPI.as_view()),
    path("addUserImages/", AddUserImages.as_view()),
    path("me/",MyProfile.as_view() ),
    path("updateProfilePicture/",UpdateProfilePicture.as_view() ),
    path("updateCoverPicture/",UpdateCoverPicture.as_view() ),
    path("updateUser/",UpdateUser.as_view() ),
    path("profile/<str:username>/follow/", FollowToggle.as_view()),
    path("profile/<str:username>/", OthersProfilePage.as_view())
]
