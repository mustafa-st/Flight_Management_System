from django.urls import path

from flight_manager.flights.v2.views import FlightsV2

urlpatterns = [
    path("flights/", FlightsV2.as_view()),
]
