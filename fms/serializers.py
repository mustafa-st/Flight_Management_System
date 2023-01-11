from rest_framework import serializers

from .models import Airport, Flight


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = (
            "origin",
            "destination",
            "flight_number",
            "departure_date_time",
            "arrival_date_time",
        )


class FlightSerializerLogin(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = "__all__"


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("iata_code", "city", "origin_airport", "destination_airport")
