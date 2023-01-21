from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from fms.filters import FlightFilter, FlightPublicFilter

from .models import Airport, Flight
from .serializers import AirportSerializer, FlightSerializer, FlightSerializerLogin

# Create your views here.


class FlightAPI(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = Flight.objects.all()
    serializer_class = FlightSerializerLogin
    filter_backends = [DjangoFilterBackend]
    filterset_class = FlightFilter


class FlightPublicAPI(generics.ListAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FlightPublicFilter


class AirportAPI(APIView):
    @staticmethod
    def get(request):
        queryset = Airport.objects.all()
        serializer = AirportSerializer(queryset, many=True)
        return Response(serializer.data, content_type="application/json")
