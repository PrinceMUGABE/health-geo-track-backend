from django.urls import path
from .views import (
    create_resource_allocation,
    get_all_allocations,
    get_allocation_by_id,
    get_allocations_by_facility,
    get_allocations_by_user,
    update_allocation,
    delete_allocation,
    get_district_sector_data,
)

urlpatterns = [
    path('allocations/', get_all_allocations, name='get_all_allocations'),
    path('create/', create_resource_allocation, name='create_resource_allocation'),
    path('<int:allocation_id>/', get_allocation_by_id, name='get_allocation_by_id'),
    path('facility/', get_allocations_by_facility, name='get_allocations_by_facility'),
    path('user/', get_allocations_by_user, name='get_allocations_by_user'),
    path('update/<int:allocation_id>/', update_allocation, name='update_allocation'),
    path('delete/<int:allocation_id>/', delete_allocation, name='delete_allocation'),
    path('district-sector-data/', get_district_sector_data, name='district-sector-data'),
]
