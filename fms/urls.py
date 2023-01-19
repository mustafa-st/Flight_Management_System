from django.urls import path

from fms.views import (
    AirportAPI,
    AuthenticatedFlightAPI,
    FlightAPI,
    NotAuthenticatedFlightAPI,
)

urlpatterns = [
    path("flights/", FlightAPI.as_view()),
    path(
        "flights/authenticated/",
        AuthenticatedFlightAPI.as_view(),
        name="AuthenticatedFlightApi",
    ),
    path(
        "flights/notAuthenticated/",
        NotAuthenticatedFlightAPI.as_view(),
        name="NotAuthenticatedFlightAPI",
    ),
    path("airports/", AirportAPI.as_view()),
]
