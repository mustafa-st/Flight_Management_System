from django_filters.rest_framework import DateFromToRangeFilter, FilterSet

from flight_manager.flights.models import Flight


class FlightFilter(FilterSet):
    departure_date_time = DateFromToRangeFilter()

    class Meta:
        model = Flight
        fields = {
            "baseFare": ["lte", "gte"],
            "flight_number": ["exact"],
            "origin__iata_code": ["exact"],
            "destination__iata_code": ["exact"],
            "departure_date_time": ["exact"],
        }


class FlightPublicFilter(FilterSet):
    departure_date_time = DateFromToRangeFilter()

    class Meta:
        model = Flight
        fields = {
            "flight_number": ["exact"],
            "origin__iata_code": ["exact"],
            "destination__iata_code": ["exact"],
            "departure_date_time": ["exact"],
        }
