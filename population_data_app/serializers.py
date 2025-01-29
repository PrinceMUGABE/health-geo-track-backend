# serializers.py
from rest_framework import serializers
from .models import PopulationData
from userApp.models import CustomUser
from health_facility_app.serializers import CustomUserSerializer

class PopulationDataSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    
    class Meta:
        model = PopulationData
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'created_by')
        
    def validate(self, data):
        """
        Validate population data consistency
        """
        if 'male_population' in data and 'female_population' in data and 'total_population' in data:
            if data['male_population'] + data['female_population'] != data['total_population']:
                raise serializers.ValidationError("Total population must match sum of male and female population")
                
        if all(key in data for key in ['children_under_5', 'youth_population', 
                                      'adult_population', 'elderly_population', 'total_population']):
            age_sum = (data['children_under_5'] + data['youth_population'] + 
                      data['adult_population'] + data['elderly_population'])
            if age_sum != data['total_population']:
                raise serializers.ValidationError("Total population must match sum of age groups")
                
        return data
