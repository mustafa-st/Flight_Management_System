from django.urls import path

from flight_manager.users.views import UserDetail, UserLogin, UserRegistration

urlpatterns = [
    path("login/", UserLogin.as_view()),
    path("signup/", UserRegistration.as_view()),
    path("detail/", UserDetail.as_view()),
]
