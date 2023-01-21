from django.db import models

# Create your models here.


class Airport(models.Model):
    iata_code = models.CharField(max_length=4, unique=True)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.city


class Flight(models.Model):
    origin = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="origin_airport"
    )
    destination = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="destination_airport"
    )
    flight_number = models.CharField(max_length=15)
    departure_date_time = models.DateTimeField()
    arrival_date_time = models.DateTimeField()
    baseFare = models.PositiveIntegerField()
    tax = models.PositiveIntegerField()

    def __str__(self):
        return self.flight_number
