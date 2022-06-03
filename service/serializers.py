from rest_framework_gis import serializers
from rest_framework import serializers as regular_serializers

from .models import Provider, ServiceArea


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = [
            'name',
            'email',
            'phone_number',
            'language',
            'currency'
        ]


class ServiceAreaSerializer(serializers.GeoFeatureModelSerializer):
    class Meta:
        model = ServiceArea
        geo_field = 'geom'
        fields = [
            'provider',
            'name',
            'price',
        ]


class PointCheckSerializer(regular_serializers.Serializer):
    latitude = regular_serializers.DecimalField(decimal_places=15, max_digits=100)
    longitude = regular_serializers.DecimalField(decimal_places=15, max_digits=100)
