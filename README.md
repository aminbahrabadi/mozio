# Simple Django GIS Provider Services API
## Problem
We have a problem that many transportation suppliers we'd like to integrate cannot give us concrete zip codes, cities, etc that they serve.
To combat this, we'd like to be able to define custom polygons as their "service area" and we'd like for the owners of these shuttle companies to be able to define and alter their polygons whenever they want.
## What we do in this repository
We have some Providers that provide services within a area (polygon area). We define providers and their area of services then we can check that what areas contain a requested point and how much costs the services in that areas and what providers can do the service in those areas.
## Live demo
You can test live demo here: [Simple Django GIS Provider Services API](https://mozio-dev.ir)
## How to run
1. Clone the project
2. Open terminal and create a virtual environment:
<br />```virtualenv venv```
3. Activate virtual environment:
<br />```source venv/bin/activate```
4. Install packages:
<br />```pip install -r requirements.txt```
5. Migrate and create database:
<br />```python manage.py migrate```
6. Run server:
<br />```python manage.py runserver```
7. You can run tests:
<br />```python manage.py test```
8. Open the browser and browse this URL:
<br />```127.0.0.1:8000```
## Api
### List of all providers (GET request):
<br />URL: ```/providers/list/```
### Provider create (POST request):
<br />URL: ```/providers/create/```
<br />Data load sample: ```{
            'name': 'test provider',
            'email': 'test@test.com',
            'phone_number': '+989360000000',
            'language': 'EN',
            'currency': 'USD'
        }```
### Provider update (PUT request):
<br />URL: ```/providers/update/<provider_id>/```
<br />Data load sample: ```{
            'name': 'test provider 2',
            'email': 'test_2@test.com',
            'phone_number': '+989350000000',
            'language': 'FR',
            'currency': 'EURO'
        }```
### Provider detail (GET request):
<br />URL: ```/providers/detail/<provider_id>/```
### Provider delete (DELETE request):
<br />URL: ```/providers/delete/<provider_id>/```
### List of service areas (GET request):
<br />URL: ```/service-area/list/```
### List of service areas of a provider (GET request):
<br />URL: ```/service-area/list/<provider_id>/```
### Service area create (POST request):
<br />URL: ```/service-area/create/```
<br />Data load sample: ```{
            "provider": provider.id,
            "name": "New Test",
            "price": 100.85,
            "geom": {
                "type": "MultiPolygon",
                "coordinates": [[[[49.8065, 35.0450], [49.5373, 34.6769], [50.7513, 34.7209], [49.8065, 35.0450]]]]
            }
        }```
### Service area update (PUT request):
<br />URL: ```/service-area/update/<service_id>```
<br />Data load sample: ```{
            "provider": 1,
            "name": "New Test",
            "price": 100.85,
            "geom": {
                "type": "MultiPolygon",
                "coordinates": [[[[49.8065, 35.0450], [49.5373, 34.6769], [50.7513, 34.7209], [49.8065, 35.0450]]]]
            }
        }```
### Service area detail (GET request):
<br />URL: ```/service-area/detail/<service_id>/```
### Service area delete (DELETE request):
<br />URL: ```/service-area/delete/<service_id>/```
### Point check (POST request):
<br />URL: ```/service-area/point-check/```
<br />Data load sample: ```{
            'latitude': 50.01796,
            'longitude': 34.84172
        }```
