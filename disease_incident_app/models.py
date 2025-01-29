# models.py
from django.db import models
from django.conf import settings
from health_facility_app.models import HealthFacility
from django.utils.timezone import now

class DiseaseIncident(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('RESOLVED', 'Resolved'),
        ('UNDER_INVESTIGATION', 'Under Investigation'),
        ('CONTAINED', 'Contained')
    ]
    
    disease_name = models.CharField(max_length=255)
    health_facility = models.ForeignKey(HealthFacility, on_delete=models.CASCADE, related_name='incidents')
    number_of_cases = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')  # Default status is 'ACTIVE'
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.disease_name} at {self.health_facility.name}"
