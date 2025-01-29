from django.urls import path
from . import views

urlpatterns = [

    path('facilities/', views.get_all_facilities, name='get-all-facilities'),
    path('add/', views.add_facility, name='add-facility'),
    path('<int:pk>/', views.get_facility_by_id, name='get-facility-by-id'),
    path('name/<str:name>/', views.get_facility_by_name, name='get-facility-by-name'),
    path('district/<str:district>/', views.get_facilities_by_district, name='get-facilities-by-district'),
    path('sector/<str:sector>/', views.get_facilities_by_sector, name='get-facilities-by-sector'),
    path('status/<str:status>/', views.get_facilities_by_status, name='get-facilities-by-status'),
    path('update/<int:pk>/', views.update_facility, name='update-facility'),
    path('delete/<int:pk>/', views.delete_facility, name='delete-facility'),
]
