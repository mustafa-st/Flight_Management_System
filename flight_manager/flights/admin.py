from django.contrib import admin

from flight_manager.flights.v1.models import (
    Airport,
    Booking,
    ContactDetail,
    Flight,
    TravelerDetail,
)

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


@admin.register(TravelerDetail)
class TravelerDetailAdmin(admin.ModelAdmin):
    list_display = ["booking", "first_name", "last_name", "age"]


@admin.register(ContactDetail)
class ContactDetailAdmin(admin.ModelAdmin):
    list_display = ["booking", "mobile_number", "email"]


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ["id"]
