from celery import shared_task

from flight_manager.flights.v1.models import Flight


@shared_task
def task1(x, y):
    return x + y


@shared_task
def task2(x):
    print(x)


@shared_task
def increment_flight_price():
    all_flights = Flight.objects.all()
    for flight in all_flights:
        price = flight.baseFare
        flight.baseFare = flight.baseFare + 100
        flight.save()
        print(
            f"Incrementing price of flight: {flight.id}. Old Price: {price}, New Price: {flight.baseFare}"
        )
