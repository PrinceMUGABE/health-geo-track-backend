from rest_framework import serializers
from health_facility_app.models import HealthFacility
from .models import AccessibilityData
from health_facility_app.models import HealthFacility
from userApp.models import CustomUser

# Serializer for the created_by user
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser()  # Fetches the custom user model
        fields = ['id', 'phone_number', 'email', 'role', 'is_active', 'is_staff', 'created_at']  # Specify desired fields

# Serializer for the health facility
class HealthFacilitySerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)  # Nest the user serializer

    class Meta:
        model = HealthFacility
        fields = '__all__'
        read_only_fields = ('id','created_at', 'created_by')
        
        

class AccessibilityDataSerializer(serializers.ModelSerializer):
    health_facility = HealthFacilitySerializer(read_only=True)
    created_by = CustomUserSerializer(read_only=True)
    accessibility_rating = serializers.CharField(read_only=True)  # Make it read-only
    health_facility_id = serializers.PrimaryKeyRelatedField(
        queryset=HealthFacility.objects.all(),
        source='health_facility',  # Maps to the foreign key
        write_only=True
    )

    class Meta:
        model = AccessibilityData
        fields = [
            'id',
            'health_facility',
            'health_facility_id',
            'people_served',
            'avg_travel_time',
            'distance_to_nearest_facility',
            'accessibility_rating',
            'created_at',
            'created_by'
        ]
        read_only_fields = ['id', 'accessibility_rating', 'created_at', 'created_by']
