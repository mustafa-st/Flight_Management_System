from django.core.cache import cache


def flights_aggregated_data(staging_flights, staging_flights_data: []):
    for i in range(len(staging_flights_data)):
        origin_iata_code = staging_flights_data[i]["legs"][0]["segments"][0]["origin"][
            "iata_code"
        ]
        destination_iata_code = staging_flights_data[i]["legs"][0]["segments"][0][
            "destination"
        ]["iata_code"]
        flight_number = staging_flights_data[i]["legs"][0]["segments"][0][
            "flight_number"
        ].pop()
        provider = staging_flights_data[i]["provider"]
        departure_date_time = staging_flights_data[i]["legs"][0]["segments"][0][
            "departure_datetime"
        ]
        arrival_date_time = staging_flights_data[i]["legs"][0]["segments"][0][
            "arrival_datetime"
        ]

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
    return staging_flights


def flights_aggregated_payload(request):
    cabinClass = request.data["search_params"][0]["cabinClass"]
    legs = request.data["search_params"][1]["legs"]
    routeType = request.data["search_params"][2]["routeType"]
    travelerCount = request.data["search_params"][3]["travelerCount"]

    payload = {
        "route_type": routeType,
        "cabin_class": cabinClass,
        "traveler_count": travelerCount,
        "legs": [legs],
    }
    return payload


def flight_providers_response(
    request, poll, abs_url, serializer, response, flights_data, staging_flights_data
):
    staging_flights = []
    if poll:
        cache.set(str(abs_url), serializer.data, 60)
        flight_response = {
            "success": response.json()["success"],
            "data": [
                {"search_params": request.data["search_params"]},
                {"flights": [flights_data]},
                {"SastaTicket Staging": [{"flights": []}], "poll": True},
            ],
        }
    else:
        flights_list = flights_aggregated_data(staging_flights, staging_flights_data)
        flight_response = {
            "success": response.json()["success"],
            "data": [
                {"search_params": request.data["search_params"]},
                {"flights": [flights_data]},
                {"SastaTicket Staging": [{"flights": [flights_list]}]},
            ],
        }
    return flight_response
