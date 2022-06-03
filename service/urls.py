from django.urls import path

from . import views

app_name = 'service'


urlpatterns = [
    # provider
    path('providers/list/', views.ProviderListView.as_view(), name='provider_list'),
    path('providers/create/', views.ProviderCreateView.as_view(), name='provider_create'),
    path('providers/update/<int:provider_id>/', views.ProviderUpdateView.as_view(), name='provider_update'),
    path('providers/detail/<int:provider_id>/', views.ProviderDetailView.as_view(), name='provider_detail'),
    path('providers/delete/<int:provider_id>/', views.ProviderDeleteView.as_view(), name='provider_delete'),

    # service area
    path('service-area/list/', views.ServiceAreaListView.as_view(), name='service_area_list'),
    path('service-area/list/<int:provider_id>/', views.ProviderServiceAreaList.as_view(),
         name='provider_service_area_list'),
    path('service-area/create/', views.ServiceAreaCreateView.as_view(), name='service_area_create'),
    path('service-area/update/<int:service_id>/', views.ServiceAreaUpdateView.as_view(), name='service_area_update'),
    path('service-area/detail/<int:service_id>/', views.ServiceAreaDetailView.as_view(), name='service_area_detail'),
    path('service-area/delete/<int:service_id>/', views.ServiceAreaDeleteView.as_view(), name='service_area_delete'),

    path('service-area/point-check/', views.PointCheckView.as_view(), name='service_area_point_check'),
]
