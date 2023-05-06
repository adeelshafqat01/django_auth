from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from apps.address.models import Country, Location, State, Town
from apps.service_providers.models import ServiceProvider

# Register your models here.


class ServiceProviderInline(admin.TabularInline):
    model = ServiceProvider
    fields = [
        "id",
        "buisness_type",
        "facility_name",
        "phone_number",
        "email",
        "website",
        "unit_numbers",
        "size",
        "working_hours",
        "service_types",
        "is_occupied",
    ]
    readonly_fields = ["id"]
    extra = 0


class LocationAdmin(LeafletGeoAdmin):
    list_display = ["id", "address", "locations"]
    inlines = [ServiceProviderInline]


admin.site.register(Country)
admin.site.register(State)
admin.site.register(Town)
admin.site.register(Location, LocationAdmin)
