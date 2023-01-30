from django.urls import include, path

from flight_manager.flights.v1.views import (
    AirportAPI,
    FlightAPI,
    FlightBooking,
    FlightPublicAPI,
)

urlpatterns = [
    path("flights/", FlightAPI.as_view()),
    path("public/v2/", include("flight_manager.flights.v2.urls")),
    path("airports/", AirportAPI.as_view()),
    path("public/flights/", FlightPublicAPI.as_view()),
    path("book/", FlightBooking.as_view()),
]
