from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .manager import UserManager

class User(AbstractUser):
    """User model."""

    GenderChoice = [('others', 'Others'),('male', 'Male'),('female' ,'Female')]

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    gender = models.CharField(max_length=10,choices=GenderChoice, default='male')
    birthDate = models.DateField(auto_now=False, auto_now_add=False)
    location = models.CharField(max_length=30, default="India")
    mobile = models.CharField(max_length=15)
    bio = models.TextField(max_length=500, default="Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolorum deserunt cum consectetur ratione quisquam accusamus ipsum, voluptates repellendus obcaecati? Minima?")
    followers = models.ManyToManyField('User', blank=True, related_name='following')
    verified = models.BooleanField(default=False)
    profilePictureUrl = models.URLField()
    coverPictureUrl = models.URLField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'birthDate', 'gender','username', 'mobile']

    objects = UserManager()


    def __str__(self):
        return f'{self.first_name} {self.last_name}'
 
    def nFollowers(self):
        return self.followers.all().count()

    def nFollowing(self):
        return self.following.all().count()