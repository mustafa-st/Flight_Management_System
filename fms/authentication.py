from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomAuthentication(JWTAuthentication, BaseAuthentication):
    def authenticate(self, request):

        token = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE"])
        if token is not None:
            validated_token = self.get_validated_token(token)
            print(validated_token)

            return self.get_user(validated_token), validated_token
        else:
            return None


class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        if request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE"]) is not None:
            print("Inside If")
            return True
        else:
            print("Inside else")
            return False
