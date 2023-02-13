from django.contrib.auth import authenticate
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from flight_manager.users.functions import get_token_for_user

from .serializers import LoginUserSerializer, UserRegisterSerializer


class UserRegistration(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            msg = {
                "success": True,
                "payload": {
                    "message": "User Created for email: {}".format(
                        serializer.validated_data["email"]
                    )
                },
            }
            return Response(msg, status=status.HTTP_200_OK)
        except Exception as exc:
            raise exc


class UserLogin(APIView):
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError(
                    "Unable to log in with provided credentials."
                )
            token = get_token_for_user(user)
            context = {
                "success": True,
                "payload": {"refresh": token["refresh"], "access": token["access"]},
            }
            return Response(context)
        except Exception as err:
            raise err
