from django.db import models
from django.conf import settings
from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from health_facility_app.models import HealthFacility
from userApp.models import CustomUser

# ResourceAllocation Model
class ResourceAllocation(models.Model):
    health_facility = models.ForeignKey(HealthFacility, on_delete=models.CASCADE, related_name='allocations')
    equipment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    specialist = models.IntegerField()
    duration_in_days = models.IntegerField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Allocation for {self.health_facility.name} on {self.date_of_allocation}" 
