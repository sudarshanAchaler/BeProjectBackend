from django.urls import path
from .views import PostAPI, DeletePost

urlpatterns = [
    path("",PostAPI.as_view()),
    path("<int:id>",DeletePost.as_view())
]