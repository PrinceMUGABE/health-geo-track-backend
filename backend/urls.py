
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('userApp.urls')),
    path('facility/', include('health_facility_app.urls')),
    path('incident/', include('disease_incident_app.urls')),
    path('population/', include('population_data_app.urls')),
    path('resource_allocation/', include('resource_allocation_app.urls')),
    path('accessibility/', include('accessiblity_app.urls')),
]