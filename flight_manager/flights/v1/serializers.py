from rest_framework import serializers

from flight_manager.flights.v1.models import (
    Airport,
    Booking,
    ContactDetail,
    Flight,
    TravelerDetail,
)


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = (
            "origin",
            "destination",
            "flight_number",
            "departure_date_time",
            "arrival_date_time",
            "provider",
        )


class FlightSerializerLogin(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = "__all__"


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("iata_code", "city", "origin_airport", "destination_airport")


class TravelerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelerDetail
        fields = ("first_name", "last_name", "age")


class ContactDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactDetail
        fields = ("mobile_number", "email")


class BookingSerializer(serializers.ModelSerializer):
    contact_detail = ContactDetailSerializer()
    traveler_detail = TravelerDetailSerializer(many=True)

    class Meta:
        model = Booking
        fields = ("traveler_detail", "contact_detail")

    def create(self, validated_data):
        travelers_data = validated_data.pop("traveler_detail")
        contact_data = validated_data.pop("contact_detail")
        booking = Booking.objects.create(**validated_data)
        if len(travelers_data) > 3:
            raise serializers.ValidationError({"error": "Max Seat limit 3"})
        ContactDetail.objects.create(booking=booking, **contact_data)
        for traveler_data in travelers_data:
            TravelerDetail.objects.create(booking=booking, **traveler_data)
        return booking
