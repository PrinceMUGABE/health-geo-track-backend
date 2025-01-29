# serializers.py
from rest_framework import serializers
from .models import DiseaseIncident
from health_facility_app.serializers import HealthFacilitySerializer, CustomUserSerializer
from health_facility_app.models import HealthFacility
from userApp.models import CustomUser

class DiseaseIncidentSerializer(serializers.ModelSerializer):
    health_facility = HealthFacilitySerializer(read_only=True)
    health_facility_id = serializers.PrimaryKeyRelatedField(
        queryset=HealthFacility.objects.all(),
        write_only=True,
        source='health_facility'
    )
    created_by = CustomUserSerializer(read_only=True)

    class Meta:
        model = DiseaseIncident
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'created_by')