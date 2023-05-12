from django.urls import path
from .views import PostAPI

urlpatterns = [
    path("",PostAPI.as_view())
]