from django.contrib.auth.hashers import make_password
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers, status

from flight_manager.users.models import User
from flight_manager.users.MyExceptions import MyCustomExcpetion


class UserRegisterSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(allow_blank=True, max_length=150)
    last_name = serializers.CharField(allow_blank=True, max_length=150)
    username = serializers.CharField(
        error_messages={"unique": "A user with that username already exists."}
    )
    mobile_number = PhoneNumberField()
    email = serializers.EmailField(allow_blank=True, max_length=254)
    password = serializers.CharField(max_length=128, min_length=8)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "mobile_number",
            "email",
            "password",
        ]

    def validate(self, attrs):
        username = attrs["username"]
        email = attrs["email"]
        user_q = User.objects.filter(username__iexact=username)
        email_q = User.objects.filter(email__iexact=email)
        if user_q.exists():
            raise MyCustomExcpetion(
                detail={
                    "success": False,
                    "error": "BAD_REQUEST: Username already exist",
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        elif email_q.exists():
            raise MyCustomExcpetion(
                detail={"success": False, "error": "BAD_REQUEST: Email already exist"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        return attrs


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(max_length=128)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            password=make_password(validated_data["password"]),
        )
        return user


class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
