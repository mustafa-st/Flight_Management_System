from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from flight_manager.flights.filters import FlightFilter, FlightPublicFilter
from flight_manager.flights.models import Airport, Flight
from flight_manager.flights.serializers import (
    AirportSerializer,
    FlightSerializer,
    FlightSerializerLogin,
)

# Create your views here.


class FlightAPI(generics.ListAPIView):
    try:
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        queryset = Flight.objects.all()
        serializer_class = FlightSerializerLogin
        filter_backends = [DjangoFilterBackend]
        filterset_class = FlightFilter

        def list(self, request, *args, **kwargs):
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response({"success": True, "payload": serializer.data})

    except Exception as exp:
        response = JsonResponse(exp.args)
        raise response


class FlightPublicAPI(generics.ListAPIView):
    # Response.writable("Hi")
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FlightPublicFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({"success": True, "payload": serializer.data})


class AirportAPI(APIView):
    @staticmethod
    def get(request):
        queryset = Airport.objects.all()
        serializer = AirportSerializer(queryset, many=True)
        return Response(serializer.data, content_type="application/json")
