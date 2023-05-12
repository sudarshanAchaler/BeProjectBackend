from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import authenticate


User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "birthDate",
            "gender",
            "mobile",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name","id", "username", "gender", "birthDate", "location", "mobile", "bio", "nFollowers", "nFollowing", "verified", "coverPictureUrl", "profilePictureUrl"]

class UserBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "id","birthDate", "verified","first_name", "last_name","username","profilePictureUrl"]


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name","username", "location", "mobile", "bio"]

class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid Credentials.")
