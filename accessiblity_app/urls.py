from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_accessibility_data, name='create_accessibility_data'),
    path("accessibilities/", views.get_all_accessibility_data, name="get_all_accessibilities"),
    path('<int:pk>/', views.get_accessibility_data_by_id, name='get_accessibility_data_by_id'),
    path('facility/', views.get_accessibility_data_by_facility, name='get_accessibility_data_by_facility'),
    path('update/<int:pk>/', views.update_accessibility_data, name='update_accessibility_data'),
    path('delete/<int:pk>/', views.delete_accessibility_data, name='delete_accessibility_data'),
    path('user/', views.get_accessibility_data_by_user, name='get_user_accessibilities'),
]
