# from django.http import HttpResponse
# from rest_framework.renderers import JSONRenderer
# from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


# def json_http_msg(message):
#     return Response(message, content_type="application/json")
