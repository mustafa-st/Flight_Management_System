from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from flight_manager.users.functions import get_token_for_user

from .serializers import LoginUserSerializer, UserRegisterSerializer

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
            # err {"success": False, "error": exc.__cause__}


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
                    {
                        "success": False,
                        "error": "Unable to log in with provided credentials.",
                    }
                )
            token = get_token_for_user(user)
            context = {
                "success": True,
                "payload": {"refresh": token["refresh"], "access": token["access"]},
            }
            return Response(context)
        except serializers.ValidationError as err:
            raise err


#
# class UserLogin(APIView):
#     # @csrf_exempt
#     def post(self, request):
#         serializer = LoginUserSerializer(data=request.JSON)
#         username = request.JSON["username"]
#         password = request.JSON["password"]
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             if serializer.is_valid():
#                 token = get_token_for_user(user)
#                 context = {
#                     "success": True,
#                     "payload": {"refresh": token["refresh"], "access": token["access"]},
#                 }
#                 return Response(context)
#         else:
#             msg = {
#                 "success": False,
#                 "error": "Invalid username or password",
#             }
#             return Response(msg, status=status.HTTP_400_BAD_REQUEST)
