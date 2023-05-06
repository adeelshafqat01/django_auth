from rest_framework import serializers

from apps.address.models import Location

from .models import ServiceProvider


class ServiceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProvider
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    location = ServiceProviderSerializer(many=True)

    class Meta:
        model = Location
        fields = ["id", "address", "locations", "location"]
        extra_kwargs = {"locations": {"read_only": True}}

    def create(self, validated_data):
        service_provider = validated_data.pop("location")
        try:
            locations_data = Location.objects.get(locations=validated_data["locations"])
            for service in service_provider:
                service.pop("locations", None)
                ServiceProvider.objects.create(locations=locations_data, **service)
        except:
            locations_data = Location.objects.create(**validated_data)
            for service in service_provider:
                service.pop("locations", None)
                ServiceProvider.objects.create(locations=locations_data, **service)
        return locations_data
