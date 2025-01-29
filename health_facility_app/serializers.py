from rest_framework import serializers
from .models import HealthFacility
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
