import requests
from django.core.cache import cache
from rest_framework.views import Response

from flight_manager.flights.v1.views import FlightPublicAPI as V1FlightPublicAPI
from flight_manager.utils.flights_aggregator import (
    flight_providers_response,
    flights_aggregated_payload,
)


class FlightPublicAPI(V1FlightPublicAPI):
    def list(self, request, *args, **kwargs):
        try:
            abs_url = request.build_absolute_uri()
            url = "https://staging.sastaticket.pk/api/v4/flights/"
            headers = {"content-type": "application/json"}
            payload = flights_aggregated_payload(request)
            response = requests.post(url, json=payload, headers=headers)

            poll = False
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            flights = cache.get(str(abs_url))
            staging_flights_data = response.json()["data"]["flights"][0]
            flights_data = []
            if flights is not None:
                flights_data = flights
            else:
                poll = True

            flight_response = flight_providers_response(
                request,
                poll,
                abs_url,
                serializer,
                response,
                flights_data,
                staging_flights_data,
            )
            return Response(flight_response)

        except Exception as exc:
            raise exc
