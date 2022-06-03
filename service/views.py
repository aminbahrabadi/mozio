from django.contrib.gis.geos import Point
from django.forms import model_to_dict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from django.shortcuts import get_object_or_404

import json

from .serializers import ProviderSerializer, ServiceAreaSerializer, PointCheckSerializer
from .models import Provider, ServiceArea


class ProviderListView(APIView):
    """
    List of all providers Api
    """
    def get(self, request, *args, **kwargs):
        providers = Provider.objects.all()
        result = {}

        for provider in providers:
            result[provider.id] = {
                'name': provider.name,
                'email': provider.email,
                'phone_number': provider.phone_number,
                'language': provider.language,
                'currency': provider.currency,
            }

        return Response(result, status=status.HTTP_200_OK)


class ProviderCreateView(APIView):
    """
    Create provider Api
    """
    def post(self, request, *args, **kwargs):
        serializer = ProviderSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            email = serializer.validated_data.get('email')
            phone_number = serializer.validated_data.get('phone_number')
            language = serializer.validated_data.get('language')
            currency = serializer.validated_data.get('currency')

            provider = Provider.objects.create(
                name=name,
                email=email,
                phone_number=phone_number,
                language=language,
                currency=currency
            )

            return Response(f'provider: {provider.name} is created!', status=status.HTTP_201_CREATED)

        return Response({'message': 'provider create failed!', 'details': serializer.errors})


class ProviderUpdateView(UpdateAPIView):
    """
    Update provider Api
    """
    serializer_class = ProviderSerializer

    def update(self, request, *args, **kwargs):
        provider_id = self.kwargs.get('provider_id')
        instance = get_object_or_404(Provider, id=provider_id)
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response('provider is updated', status=status.HTTP_200_OK)

        return Response({'message': 'provider update failed!', 'details': serializer.errors})


class ProviderDetailView(APIView):
    """
    Provider Detail Api
    """
    def get(self, request, *args, **kwargs):
        provider_id = self.kwargs.get('provider_id')
        provider = get_object_or_404(Provider, id=provider_id)

        return Response(model_to_dict(provider), status=status.HTTP_200_OK)


class ProviderDeleteView(APIView):
    """
    Delete provider Api
    """
    def delete(self, request, *args, **kwargs):
        provider_id = self.kwargs.get('provider_id')
        provider = get_object_or_404(Provider, id=provider_id)
        provider.delete()

        return Response('provider is deleted', status=status.HTTP_200_OK)


class ServiceAreaListView(APIView):
    """
    List of all service areas Api
    """
    def get(self, request, *args, **kwargs):
        services = ServiceArea.objects.all()
        result = {}

        for service in services:
            result[service.id] = {
                'name': service.name,
                'provider': service.provider.name,
                'price': service.price,
                'geom': json.loads(service.geom.json)
            }

        return Response(result, status=status.HTTP_200_OK)


class ProviderServiceAreaList(APIView):
    """
    List of all provider's service areas Api
    """
    def get(self, request, *args, **kwargs):
        provider_id = self.kwargs.get('provider_id')
        provide_services = ServiceArea.objects.filter(provider_id=provider_id)

        result = {}

        for service in provide_services:
            result[service.id] = {
                'name': service.name,
                'provider': service.provider.name,
                'price': service.price,
                'geom': json.loads(service.geom.json)
            }

        return Response(result, status=status.HTTP_200_OK)


class ServiceAreaCreateView(APIView):
    """
    Create service area Api
    """
    def post(self, request, *args, **kwargs):
        serializer = ServiceAreaSerializer(data=request.data)

        if serializer.is_valid():
            provider = serializer.validated_data.get('provider')
            name = serializer.validated_data.get('name')
            price = serializer.validated_data.get('price')
            geom = serializer.validated_data.get('geom')

            service = ServiceArea.objects.create(
                provider=provider,
                name=name,
                price=price,
                geom=geom
            )

            return Response(f'area_service: {service.name} is created!', status=status.HTTP_201_CREATED)

        return Response({'message': 'service create failed!', 'details': serializer.errors})


class ServiceAreaUpdateView(UpdateAPIView):
    """
    Update service area Api
    """
    serializer_class = ServiceAreaSerializer

    def update(self, request, *args, **kwargs):
        service_id = self.kwargs.get('service_id')
        instance = get_object_or_404(ServiceArea, id=service_id)
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response('service_area is updated', status=status.HTTP_200_OK)

        return Response({'message': 'service_area update failed!', 'details': serializer.errors})


class ServiceAreaDetailView(APIView):
    """
    Service area detail Api
    """
    def get(self, request, *args, **kwargs):
        service_id = self.kwargs.get('service_id')
        service = get_object_or_404(ServiceArea, id=service_id)

        result = {
            'name': service.name,
            'provider': service.provider.name,
            'price': service.price,
            'geom': json.loads(service.geom.json)
        }

        return Response(result, status=status.HTTP_200_OK)


class ServiceAreaDeleteView(APIView):
    """
    Delete service area
    """
    def delete(self, request, *args, **kwargs):
        service_id = self.kwargs.get('service_id')
        service = get_object_or_404(ServiceArea, id=service_id)
        service.delete()

        return Response('service_area is deleted', status=status.HTTP_200_OK)


class PointCheckView(APIView):
    """
    Point check Api, check what polygons contains the point
    """
    def post(self, request, *args, **kwargs):
        serializer = PointCheckSerializer(data=request.data)

        if serializer.is_valid():
            latitude = serializer.validated_data.get('latitude')
            longitude = serializer.validated_data.get('longitude')

            point = Point(float(latitude), float(longitude))

            areas = ServiceArea.objects.filter(geom__contains=point)

            result = {}

            for area in areas:
                result[area.id] = {
                    'name': area.name,
                    'provider': area.provider.name,
                    'price': area.price,
                    'geom': json.loads(area.geom.json)
                }

            return Response(result, status=status.HTTP_200_OK)

        return Response({'message': 'point check failed!', 'details': serializer.errors})
