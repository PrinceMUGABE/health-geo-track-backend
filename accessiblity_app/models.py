from django.db import models
from django.conf import settings
from health_facility_app.models import HealthFacility

class AccessibilityData(models.Model):
    health_facility = models.ForeignKey(HealthFacility, on_delete=models.CASCADE, related_name='accessibility_data')
    people_served = models.IntegerField()
    avg_travel_time = models.FloatField(help_text="Average travel time in minutes")
    distance_to_nearest_facility = models.FloatField(help_text="Distance to the nearest facility in kilometers")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Remove accessibility_rating from the input fields
    ACCESSIBILITY_RATING_CHOICES = [
        ('GOOD', 'Good'),
        ('MODERATE', 'Moderate'),
        ('POOR', 'Poor'),
    ]
    accessibility_rating = models.CharField(max_length=20, choices=ACCESSIBILITY_RATING_CHOICES, editable=False)

    def save(self, *args, **kwargs):
        # Calculate the accessibility rating before saving
        self.accessibility_rating = self.calculate_rating()
        super().save(*args, **kwargs)

    def calculate_rating(self):
        """
        A custom method to calculate the accessibility rating.
        - GOOD: Travel time <= 15 mins and distance <= 5 km
        - MODERATE: Travel time <= 30 mins and distance <= 10 km
        - POOR: Otherwise
        """
        if self.avg_travel_time <= 15 and self.distance_to_nearest_facility <= 5:
            return 'GOOD'
        elif self.avg_travel_time <= 30 and self.distance_to_nearest_facility <= 10:
            return 'MODERATE'
        else:
            return 'POOR'

    def __str__(self):
        return f"Accessibility data for {self.health_facility.name}"
