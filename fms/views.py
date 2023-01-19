from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

from fms.authentication import CustomAuthentication, CustomPermission

from .models import Airport, Flight
from .serializers import AirportSerializer, FlightSerializer, FlightSerializerLogin

# Create your views here.


class AuthenticatedFlightAPI(generics.ListAPIView):
    authentication_classes = [CustomAuthentication]
    queryset = Flight.objects.all()
    serializer_class = FlightSerializerLogin
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "flight_number",
        "origin__iata_code",
        "destination__iata_code",
        "departure_date_time",
    ]


class NotAuthenticatedFlightAPI(generics.ListAPIView):
    authentication_classes = [CustomAuthentication]
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "flight_number",
        "origin__iata_code",
        "destination__iata_code",
        "departure_date_time",
    ]


class FlightAPI(generics.ListAPIView):
    permission_classes = [CustomPermission]
    queryset = Flight.objects.all()

    if permission_classes is True:
        serializer_class = FlightSerializerLogin
    else:
        serializer_class = FlightSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "flight_number",
        "origin__iata_code",
        "destination__iata_code",
        "departure_date_time",
    ]


class AirportAPI(APIView):
    @staticmethod
    def get(request):
        queryset = Airport.objects.all()
        serializer = AirportSerializer(queryset, many=True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type="application/json")
