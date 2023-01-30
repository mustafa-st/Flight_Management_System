import requests
from django.core.cache import cache
from rest_framework.views import Response

from flight_manager.flights.v1.views import FlightPublicAPI as V1FlightPublicAPI


class FlightPublicAPI(V1FlightPublicAPI):
    def list(self, request, *args, **kwargs):
        try:
            abs_url = request.build_absolute_uri()
            cabinClass = request.data["search_params"][0]["cabinClass"]
            legs = request.data["search_params"][1]["legs"]
            routeType = request.data["search_params"][2]["routeType"]
            travelerCount = request.data["search_params"][3]["travelerCount"]

            url = "https://staging.sastaticket.pk/api/v4/flights/"
            headers = {"content-type": "application/json"}
            payload = {
                "route_type": routeType,
                "cabin_class": cabinClass,
                "traveler_count": travelerCount,
                "legs": [legs],
            }
            r = requests.post(url, json=payload, headers=headers)

            poll = False
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            flights = cache.get(str(abs_url))
            print(len(r.json()["data"]["flights"][0]))
            staging_flights = []

            if flights is not None:
                flights_data = flights
            else:
                flights_data = []
                poll = True

            if poll:
                cache.set(str(abs_url), serializer.data, 60)
                flight_response = {
                    "success": r.json()["success"],
                    "data": [
                        {"search_params": request.data["search_params"]},
                        {"flights": [flights_data], "poll": True},
                        {"SastaTicket Staging": [{"flights": []}]},
                    ],
                }
            else:
                for i in range(len(r.json()["data"]["flights"][0])):
                    origin_iata_code = r.json()["data"]["flights"][0][i]["legs"][0][
                        "segments"
                    ][0]["origin"]["iata_code"]
                    destination_iata_code = r.json()["data"]["flights"][0][i]["legs"][
                        0
                    ]["segments"][0]["destination"]["iata_code"]
                    flight_number = r.json()["data"]["flights"][0][i]["legs"][0][
                        "segments"
                    ][0]["flight_number"].pop()
                    provider = r.json()["data"]["flights"][0][i]["provider"]
                    departure_date_time = r.json()["data"]["flights"][0][i]["legs"][0][
                        "segments"
                    ][0]["departure_datetime"]
                    arrival_date_time = r.json()["data"]["flights"][0][i]["legs"][0][
                        "segments"
                    ][0]["arrival_datetime"]

                    staging_flights.append(
                        {
                            "origin": origin_iata_code,
                            "destination": destination_iata_code,
                            "flight_number": flight_number,
                            "departure_date_time": departure_date_time,
                            "arrival_date_time": arrival_date_time,
                            "provider": provider,
                        }
                    )

                flight_response = {
                    "success": r.json()["success"],
                    "data": [
                        {"search_params": request.data["search_params"]},
                        {"flights": [flights_data]},
                        {"SastaTicket Staging": [{"flights": [staging_flights]}]},
                    ],
                }

            return Response(flight_response)

        except Exception as exc:
            raise exc
