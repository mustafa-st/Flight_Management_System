from django.contrib import admin

from fms.models import Airport, Flight

# Register your models here.


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = [
        "origin",
        "destination",
        "flight_number",
        "departure_date_time",
        "arrival_date_time",
        "baseFare",
        "tax",
    ]


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ["iata_code", "city"]
