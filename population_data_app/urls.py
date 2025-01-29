# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('populations/', views.get_all_populations, name='get-all-populations'),
    path('add/', views.add_population, name='add-population'),
    path('<int:pk>/', views.get_population_by_id, name='get-population-by-id'),
    path('user/', views.get_populations_by_user, name='get-populations-by-user'),
    path('district/<str:district>/', views.get_populations_by_district, name='get-populations-by-district'),
    path('sector/<str:sector>/', views.get_populations_by_sector, name='get-populations-by-sector'),
    path('status/<str:status_value>/', views.get_populations_by_socioeconomic_status, name='get-populations-by-status'),
    path('update/<int:pk>/', views.update_population, name='update-population'),
    path('delete/<int:pk>/', views.delete_population, name='delete-population'),
]