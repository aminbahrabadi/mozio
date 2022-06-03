from rest_framework.test import APITestCase, APIClient
from django.urls import reverse

from django.contrib.gis.geos import Polygon, MultiPolygon

from .models import Provider, ServiceArea


class TestServiceViews(APITestCase):
    """
    Client tests of ticket views
    """
    def setUp(self) -> None:
        super(TestServiceViews, self).setUp()
        self.client = APIClient()

    def create_provider(self):
        provider = Provider.objects.create(
            name='test provider',
            email='test@test.com',
            phone_number='+989360000000',
            language='EN',
            currency='USD'
        )
        return provider

    def create_service_area(self):
        provider = self.create_provider()
        polygon = Polygon(((49.8065, 35.0450), (49.5373, 34.6769), (50.7513, 34.7209), (49.8065, 35.0450)))
        multi_polygon = MultiPolygon(polygon)
        service_area = ServiceArea.objects.create(
            provider=provider,
            name='Test Service',
            price=19.99,
            geom=multi_polygon
        )
        return service_area

    def test_provider_create(self):
        provider_create_url = reverse('service:provider_create')

        response = self.client.post(provider_create_url, {
            'name': 'test provider',
            'email': 'test@test.com',
            'phone_number': '+989360000000',
            'language': 'EN',
            'currency': 'USD'
        })

        providers = Provider.objects.all()

        self.assertEqual(response.status_code, 201)
        self.assertTrue(providers.exists())
        self.assertEqual(providers[0].name, 'test provider')
        self.assertEqual(providers[0].email, 'test@test.com')
        self.assertEqual(providers[0].phone_number, '+989360000000')
        self.assertEqual(providers[0].language, 'EN')
        self.assertEqual(providers[0].currency, 'USD')

    def test_provider_update(self):
        provider = self.create_provider()

        provider_update_url = reverse('service:provider_update', kwargs={'provider_id': provider.id})

        response = self.client.put(provider_update_url, {
            'name': 'test provider 2',
            'email': 'test_2@test.com',
            'phone_number': '+989350000000',
            'language': 'FR',
            'currency': 'EURO'
        })

        updated_provider = Provider.objects.all()[0]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(provider.id, updated_provider.id)
        self.assertEqual(updated_provider.name, 'test provider 2')

    def test_provider_list(self):
        provider_list_url = reverse('service:provider_list')
        provider = self.create_provider()

        response = self.client.get(provider_list_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[f'{provider.id}']['name'], 'test provider')
        self.assertEqual(response.json()[f'{provider.id}']['language'], 'EN')

    def test_service_area_create(self):
        provider = self.create_provider()
        service_area_create_url = reverse('service:service_area_create')

        response = self.client.post(service_area_create_url, format='json', data={
            "provider": provider.id,
            "name": "New Test",
            "price": 100.85,
            "geom": {
                "type": "MultiPolygon",
                "coordinates": [[[[49.8065, 35.0450], [49.5373, 34.6769], [50.7513, 34.7209], [49.8065, 35.0450]]]]
            }
        })

        created_service_area = ServiceArea.objects.all()[0]
        self.assertEqual(response.status_code, 201)
        self.assertEqual(created_service_area.name, 'New Test')

    def test_service_area_update(self):
        service_area = self.create_service_area()
        service_area_update_url = reverse('service:service_area_update', kwargs={'service_id': service_area.id})

        response = self.client.put(service_area_update_url, data={
            'name': 'Updated Service',
        })

        updated_service = ServiceArea.objects.all()[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(updated_service.name, 'Updated Service')

    def test_point_check(self):
        point_check_url = reverse('service:service_area_point_check')
        service_area = self.create_service_area()

        response = self.client.post(point_check_url, data={
            'latitude': 50.01796,
            'longitude': 34.84172
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[f'{service_area.id}']['name'], 'Test Service')
