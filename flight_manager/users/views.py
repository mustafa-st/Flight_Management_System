import phonenumbers
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, RedirectView, UpdateView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from flight_manager.users.functions import get_token_for_user

from .serializers import GetUserSerializer, LoginUserSerializer, UserRegisterSerializer

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert (
            self.request.user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self, **kwargs):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class UserRegistration(APIView):
    @csrf_exempt
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.JSON)
        if serializer.is_valid():
            serializer.save()
            msg = {
                "success": True,
                "payload": {
                    "message": "User Created for email: {}".format(
                        request.JSON["email"]
                    )
                },
            }
            return Response(msg)
        else:
            phone_number = phonenumbers.parse(request.JSON["mobile_number"])
            if not phonenumbers.is_possible_number(phone_number):
                msg = {"success": False, "error": "BAD REQUEST: Invalid Phone number"}
            else:
                msg = {
                    "success": False,
                    "error": "BAD REQUEST: Ensure password has at least 8 characters",
                }
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    @csrf_exempt
    def post(self, request):
        response = Response()
        serializer = LoginUserSerializer(data=request.JSON)
        username = request.JSON["username"]
        password = request.JSON["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            if serializer.is_valid():
                token = get_token_for_user(user)
                response.set_cookie(
                    key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                    value=token["access"],
                    domain=settings.SIMPLE_JWT["AUTH_COOKIE_DOMAIN"],
                    path=settings.SIMPLE_JWT["AUTH_COOKIE_PATH"],
                    expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                    httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                    secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                )
                response.data = {
                    "success": True,
                    "payload": {"refresh": token["refresh"], "access": token["access"]},
                }
                return response
        else:
            msg = {
                "success": False,
                "error": "BAD REQUEST: Invalid username or password",
            }
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @staticmethod
    def get(request):
        queryset = User.objects.all()
        serializer = GetUserSerializer(queryset, many=True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type="application/json")
