# views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models import DiseaseIncident, HealthFacility
from .serializers import DiseaseIncidentSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_incident(request):
    try:
        serializer = DiseaseIncidentSerializer(data=request.data)
        if serializer.is_valid():
            # Validate health facility exists
            health_facility_id = request.data.get('health_facility_id')
            if not HealthFacility.objects.filter(id=health_facility_id).exists():
                return Response(
                    {'error': 'Health facility not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Validate number of cases is positive
            number_of_cases = request.data.get('number_of_cases')
            if number_of_cases is None or int(number_of_cases) < 0:
                return Response(
                    {'error': 'Number of cases must be a positive integer'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Save the incident
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Validation Errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print("Unexpected Error:", str(e))
        return Response(
            {'error': f'Failed to create incident: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_incidents(request):
    try:
        incidents = DiseaseIncident.objects.all().select_related('health_facility', 'created_by')
        if not incidents.exists():
            return Response(
                {'message': 'No incidents found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = DiseaseIncidentSerializer(incidents, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': f'Failed to retrieve incidents: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_incident_by_id(request, pk):
    try:
        incident = get_object_or_404(
            DiseaseIncident.objects.select_related('health_facility', 'created_by'),
            pk=pk
        )
        serializer = DiseaseIncidentSerializer(incident)
        return Response(serializer.data)
    except DiseaseIncident.DoesNotExist:
        return Response(
            {'error': f'Incident with ID {pk} not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': f'Failed to retrieve incident: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_incidents_by_user(request):
    try:
        incidents = DiseaseIncident.objects.filter(
            created_by=request.user
        ).select_related('health_facility', 'created_by')
        
        if not incidents.exists():
            return Response(
                {'message': 'No incidents found for this user'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        serializer = DiseaseIncidentSerializer(incidents, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': f'Failed to retrieve user incidents: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_incidents_by_facility(request, facility_id):
    try:
        if not HealthFacility.objects.filter(id=facility_id).exists():
            return Response(
                {'error': f'Health facility with ID {facility_id} not found'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        incidents = DiseaseIncident.objects.filter(
            health_facility_id=facility_id
        ).select_related('health_facility', 'created_by')
        
        if not incidents.exists():
            return Response(
                {'message': f'No incidents found for facility ID {facility_id}'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        serializer = DiseaseIncidentSerializer(incidents, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': f'Failed to retrieve facility incidents: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_incidents_by_facility_name(request, facility_name):
    try:
        # Case-insensitive partial match for facility name
        facilities = HealthFacility.objects.filter(name__icontains=facility_name)
        
        if not facilities.exists():
            return Response(
                {'error': f'No health facilities found with name containing "{facility_name}"'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        incidents = DiseaseIncident.objects.filter(
            health_facility__in=facilities
        ).select_related('health_facility', 'created_by')
        
        if not incidents.exists():
            return Response(
                {'message': f'No incidents found for facilities matching "{facility_name}"'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        serializer = DiseaseIncidentSerializer(incidents, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': f'Failed to retrieve facility incidents: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_incidents_by_district(request, district):
    try:
        incidents = DiseaseIncident.objects.filter(
            health_facility__district__iexact=district
        ).select_related('health_facility', 'created_by')
        
        if not incidents.exists():
            return Response(
                {'message': f'No incidents found in district "{district}"'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        serializer = DiseaseIncidentSerializer(incidents, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': f'Failed to retrieve district incidents: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_incidents_by_sector(request, sector):
    try:
        incidents = DiseaseIncident.objects.filter(
            health_facility__sector__iexact=sector
        ).select_related('health_facility', 'created_by')
        
        if not incidents.exists():
            return Response(
                {'message': f'No incidents found in sector "{sector}"'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        serializer = DiseaseIncidentSerializer(incidents, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': f'Failed to retrieve sector incidents: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_incidents_by_disease(request, disease_name):
    try:
        incidents = DiseaseIncident.objects.filter(
            disease_name__icontains=disease_name
        ).select_related('health_facility', 'created_by')
        
        if not incidents.exists():
            return Response(
                {'message': f'No incidents found for disease "{disease_name}"'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        serializer = DiseaseIncidentSerializer(incidents, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': f'Failed to retrieve disease incidents: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_incidents_by_status(request, status_value):
    try:
        if status_value not in dict(DiseaseIncident.STATUS_CHOICES):
            return Response(
                {'error': f'Invalid status value: {status_value}'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        incidents = DiseaseIncident.objects.filter(
            status__iexact=status_value
        ).select_related('health_facility', 'created_by')
        
        if not incidents.exists():
            return Response(
                {'message': f'No incidents found with status "{status_value}"'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        serializer = DiseaseIncidentSerializer(incidents, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': f'Failed to retrieve status incidents: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_incident(request, pk):
    try:
        incident = get_object_or_404(DiseaseIncident, pk=pk)
        
        # Validate number of cases if provided
        if 'number_of_cases' in request.data and request.data['number_of_cases'] < 0:
            return Response(
                {'error': 'Number of cases cannot be negative'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Validate status if provided
        if 'status' in request.data and request.data['status'] not in dict(DiseaseIncident.STATUS_CHOICES):
            return Response(
                {'error': f'Invalid status value: {request.data["status"]}'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        serializer = DiseaseIncidentSerializer(incident, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except DiseaseIncident.DoesNotExist:
        return Response(
            {'error': f'Incident with ID {pk} not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': f'Failed to update incident: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_incident(request, pk):
    try:
        incident = get_object_or_404(DiseaseIncident, pk=pk)
        incident.delete()
        return Response(
            {'message': f'Incident with ID {pk} successfully deleted'},
            status=status.HTTP_204_NO_CONTENT
        )
    except DiseaseIncident.DoesNotExist:
        return Response(
            {'error': f'Incident with ID {pk} not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': f'Failed to delete incident: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )