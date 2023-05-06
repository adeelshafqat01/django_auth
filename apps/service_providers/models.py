from django.contrib.gis.db import models
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)

from apps.address.models import Location


class ServiceTypes(models.Model):
    climate_control = models.BooleanField(default=False)
    inside_service = models.BooleanField(default=False)
    outside_service = models.BooleanField(default=False)


class ServiceProvider(models.Model):
    buisness_choices = (
        ("MOVERS", "movers"),
        ("STORAGE_UNIT", "storage_unit"),
        ("ORGANIZERS", "organizers"),
    )
    buisness_type = models.CharField(max_length=255, choices=buisness_choices)
    facility_name = models.CharField(max_length=255)
    locations = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="location",
    )
    area_code = models.CharField(max_length=255, blank=True, null=True)
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'",
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    fax_number = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=254)
    website = models.URLField(max_length=200, blank=True, null=True)
    facebook = models.URLField(max_length=200, blank=True, null=True)
    instagram = models.URLField(max_length=200, blank=True, null=True)
    twitter = models.URLField(max_length=200, blank=True, null=True)
    google_buisness = models.CharField(max_length=200, blank=True, null=True)
    unit_numbers = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(111111)]
    )
    size = models.CharField(max_length=10)
    working_hours = models.CharField(max_length=200)
    service_types = models.ForeignKey(
        ServiceTypes,
        on_delete=models.SET_NULL,
        related_name="providers",
        blank=True,
        null=True,
    )
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.buisness_type}  {self.facility_name}"
