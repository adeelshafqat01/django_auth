from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

# from .forms import ServiceProviderForm
from .models import ServiceProvider, ServiceTypes

admin.site.register(ServiceTypes)


class ServiceProviderAdmin(LeafletGeoAdmin):
    list_display = [
        "id",
        "buisness_type",
        "facility_name",
        "area_code",
        "phone_number",
        "fax_number",
        "email",
        "website",
        "facebook",
        "instagram",
        "twitter",
        "google_buisness",
        "unit_numbers",
        "size",
        "working_hours",
        "service_types",
        "is_occupied",
    ]


admin.site.register(ServiceProvider, ServiceProviderAdmin)
