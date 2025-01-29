from django.db import models
from django.conf import settings

class HealthFacility(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('MAINTENANCE', 'Under Maintenance'),
        ('CLOSED', 'Closed')
    ]
    
    FACILITY_TYPES = [
        ('HOSPITAL', 'Hospital'),
        ('CLINIC', 'Clinic'),
        ('HEALTH_CENTER', 'Health Center'),
        ('PHARMACY', 'Pharmacy')
    ]
    
    name = models.CharField(max_length=255)
    facility_type = models.CharField(max_length=50, choices=FACILITY_TYPES)
    district = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    capacity = models.IntegerField()
    contact_number = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    
    def __str__(self):
        return self.name
