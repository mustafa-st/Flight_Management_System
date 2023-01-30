from django.urls import path

from flight_manager.flights.v2.views import FlightPublicAPI

urlpatterns = [
    path("flights/", FlightPublicAPI.as_view()),
]
