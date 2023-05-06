from django.contrib.gis.db import models


class Country(models.Model):
    name = models.CharField(unique=True, max_length=250)

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(unique=True, max_length=250)

    def __str__(self):
        return self.name


class Town(models.Model):
    name = models.CharField(unique=True, max_length=250)

    def __str__(self):
        return self.name


class Location(models.Model):
    address = models.CharField(max_length=255, blank=True, null=True)
    locations = models.PointField(blank=True, null=True)

    def __str__(self):
        return f"{self.address} "
