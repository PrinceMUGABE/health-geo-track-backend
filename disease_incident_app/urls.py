# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('incidents/', views.get_all_incidents, name='get-all-incidents'),
    path('add/', views.add_incident, name='add-incident'),
    path('<int:pk>/', views.get_incident_by_id, name='get-incident-by-id'),
    path('user/', views.get_incidents_by_user, name='get-incidents-by-user'),
    path('facility/<int:facility_id>/', views.get_incidents_by_facility, name='get-incidents-by-facility'),
    path('district/<str:district>/', views.get_incidents_by_district, name='get-incidents-by-district'),
    path('sector/<str:sector>/', views.get_incidents_by_sector, name='get-incidents-by-sector'),
    path('disease/<str:disease_name>/', views.get_incidents_by_disease, name='get-incidents-by-disease'),
    path('status/<str:status>/', views.get_incidents_by_status, name='get-incidents-by-status'),
    path('<int:pk>/update/', views.update_incident, name='update-incident'),
    path('<int:pk>/delete/', views.delete_incident, name='delete-incident'),
]