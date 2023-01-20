from django.urls import path

from fms.views import AirportAPI, FlightAPI, FlightPublicAPI

urlpatterns = [
    path("flights/", FlightAPI.as_view({"get": "list"})),
    path("airports/", AirportAPI.as_view()),
    path("public/flights/", FlightPublicAPI.as_view()),
]
