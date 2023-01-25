from django.urls import path

from flight_manager.flights.views import AirportAPI, FlightAPI, FlightPublicAPI

urlpatterns = [
    path("flights/", FlightAPI.as_view()),
    path("airports/", AirportAPI.as_view()),
    path("public/flights/", FlightPublicAPI.as_view()),
]
