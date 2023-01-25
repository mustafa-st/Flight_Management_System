from django.urls import path

from flight_manager.users.views import UserLogin, UserRegistration

urlpatterns = [
    path("login/", UserLogin.as_view()),
    path("signup/", UserRegistration.as_view()),
]
