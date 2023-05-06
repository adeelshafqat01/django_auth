from django.contrib.gis.geos import Point
from geopy.geocoders import Nominatim
from rest_framework import generics
from rest_framework.permissions import AllowAny

from apps.address.models import Location

from .models import ServiceProvider
from .serializers import LocationSerializer

geolocator = Nominatim(user_agent="location")


"""class ListServiceProviders(generics.ListAPIView):
    queryset = ServiceProvider.objects.all()
    serializer_class = ServiceProviderSerializer
    permission_classes = [AllowAny]
"""


class CreateServiceProviders(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        address = serializer.initial_data["address"]
        g = geolocator.geocode(address)
        lat = g.latitude
        lng = g.longitude
        pnt = Point(lng, lat)
        print(pnt)
        serializer.save(locations=pnt)


"""class UpdateServiceRetreiveView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceProvider.objects.all()
    serializer_class = ServiceProviderSerializer
    permission_classes = [AllowAny]

    def perform_update(self, serializer):
        address = serializer.initial_data["locations"]["address"]
        g = geolocator.geocode(address)
        lat = g.latitude
        lng = g.longitude
        pnt = Point(lng, lat)
        serializer.save(locations=pnt)"""
