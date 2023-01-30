from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from flight_manager.flights.v1.filters import FlightFilter, FlightPublicFilter
from flight_manager.flights.v1.models import Airport, Flight
from flight_manager.flights.v1.serializers import (
    AirportSerializer,
    BookingSerializer,
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

    except Exception as exc:
        raise exc


class FlightPublicAPI(generics.ListAPIView):
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


class FlightBooking(APIView):
    def post(self, request):
        queryset = Flight.objects.get(id=request.data["flight_number"])
        flight_serializer = FlightSerializer(queryset, many=False)
        booking_serializer = BookingSerializer(data=request.data["booking"], many=False)
        try:
            booking_serializer.is_valid(raise_exception=True)
            booking_serializer.save()
            msg = {
                "success": True,
                "payload": [
                    {
                        "message": "Flight booked against email: {}".format(
                            booking_serializer.validated_data["contact_detail"]["email"]
                        )
                    },
                    {"Flight Details": flight_serializer.data},
                    {
                        "Contact Details": booking_serializer.validated_data[
                            "contact_detail"
                        ]
                    },
                    {
                        "Traveler Details": booking_serializer.validated_data[
                            "traveler_detail"
                        ]
                    },
                ],
            }
            return Response(msg, content_type="application/json")
        except Exception as exc:
            raise exc
