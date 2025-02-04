# Serializer for ResourceAllocation
from .models import ResourceAllocation
from rest_framework import serializers
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


class ResourceAllocationSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    health_facility = HealthFacilitySerializer(read_only=True)  # Nested serializer
    health_facility_id = serializers.PrimaryKeyRelatedField(
        queryset=HealthFacility.objects.all(),
        source='health_facility',  # Maps to the foreign key
        write_only=True
    )

    class Meta:
        model = ResourceAllocation
        fields = ['id', 'health_facility', 'health_facility_id', 'equipment', 'specialist', 'duration_in_days', 'created_by', 'created_at']
        read_only_fields = ['id', 'created_by', 'created_at']
