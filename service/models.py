from django.contrib.gis.db import models
from django.db.models import Manager as GeoManager


class Provider(models.Model):
    name = models.CharField(max_length=255, null=True, blank=False, verbose_name='Name')
    email = models.EmailField(null=True, blank=False, verbose_name='Email')
    phone_number = models.CharField(max_length=15, null=True, blank=False, verbose_name='Phone Number')
    language = models.CharField(max_length=100, default='English', verbose_name='Language')
    currency = models.CharField(max_length=100, default='USD', verbose_name='Currency')

    def __str__(self):
        return self.name


class ServiceArea(models.Model):
    provider = models.ForeignKey(Provider, null=True, blank=False, on_delete=models.CASCADE, verbose_name='Provider')
    name = models.CharField(max_length=255, null=True, blank=False, verbose_name='Name')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False, verbose_name='Price')
    geom = models.MultiPolygonField(srid=4326, blank=True, null=True)

    objects = GeoManager()

    def __str__(self):
        return self.name
