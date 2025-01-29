from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import ResourceAllocation
from health_facility_app.models import HealthFacility
from .serializers import ResourceAllocationSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_resource_allocation(request):
    try:
        data = request.data
        health_facility_id = data.get('health_facility_id')

        # Validate the health_facility_id
        if not health_facility_id:
            return Response({"error": "Health facility ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            facility = HealthFacility.objects.get(id=health_facility_id)
        except HealthFacility.DoesNotExist:
            return Response({"error": f"Health facility with ID {health_facility_id} does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Prepare serializer
        serializer = ResourceAllocationSerializer(data=data)

        if serializer.is_valid():
            # Save with the current user as `created_by`
            serializer.save(health_facility=facility, created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_allocations(request):
    try:
        allocations = ResourceAllocation.objects.all()
        serializer = ResourceAllocationSerializer(allocations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": f"Error retrieving allocations: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_allocation_by_id(request, allocation_id):
    try:
        allocation = ResourceAllocation.objects.get(id=allocation_id)
        serializer = ResourceAllocationSerializer(allocation)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({"error": f"Allocation with ID {allocation_id} not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": f"Error retrieving allocation: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_allocations_by_facility(request):
    try:
        facility_name = request.data.get('facility_name')

        # Validate facility name
        if not facility_name:
            return Response({"error": "Facility name is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch health facility by name
        facility = HealthFacility.objects.filter(name__iexact=facility_name).first()
        if not facility:
            return Response({"error": f"No health facility found with the name '{facility_name}'."}, status=status.HTTP_404_NOT_FOUND)

        allocations = ResourceAllocation.objects.filter(health_facility=facility)
        serializer = ResourceAllocationSerializer(allocations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": f"Error retrieving allocations: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_allocations_by_user(request):
    try:
        allocations = ResourceAllocation.objects.filter(created_by=request.user)
        serializer = ResourceAllocationSerializer(allocations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": f"Error retrieving user allocations: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_allocation(request, allocation_id):
    try:
        allocation = ResourceAllocation.objects.get(id=allocation_id)
        
        # Ensure only the creator can update
        if allocation.created_by != request.user:
            return Response({"error": "You are not authorized to update this allocation."}, status=status.HTTP_403_FORBIDDEN)

        serializer = ResourceAllocationSerializer(allocation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response({"error": f"Allocation with ID {allocation_id} not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": f"Error updating allocation: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_allocation(request, allocation_id):
    try:
        allocation = ResourceAllocation.objects.get(id=allocation_id)
        
        # Ensure only the creator can delete
        if allocation.created_by != request.user:
            return Response({"error": "You are not authorized to delete this allocation."}, status=status.HTTP_403_FORBIDDEN)

        allocation.delete()
        return Response({"message": "Allocation deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist:
        return Response({"error": f"Allocation with ID {allocation_id} not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": f"Error deleting allocation: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)













from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Avg
from disease_incident_app.models import DiseaseIncident
from population_data_app.models import PopulationData
from accessiblity_app.models import AccessibilityData
from accessiblity_app.serializers import AccessibilityDataSerializer
from population_data_app.serializers import PopulationDataSerializer
from health_facility_app.serializers import HealthFacilitySerializer
from disease_incident_app.serializers import DiseaseIncidentSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_district_sector_data(request):
    """
    Get all related information for a specific district and sector.
    
    Required query parameters:
    - district: District name
    - sector: Sector name
    """
    district = request.query_params.get('district')
    sector = request.query_params.get('sector')
    
    if not district or not sector:
        return Response(
            {"error": "Both district and sector parameters are required"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Get population data
        population_data = PopulationData.objects.filter(
            district=district,
            sector=sector
        ).first()
        
        # Get health facilities
        health_facilities = HealthFacility.objects.filter(
            district=district,
            sector=sector
        )
        
        # Group the health facilities by their type
        grouped_health_facilities = {}
        for facility in health_facilities:
            if facility.facility_type not in grouped_health_facilities:
                grouped_health_facilities[facility.facility_type] = []
            grouped_health_facilities[facility.facility_type].append(facility)

        # Get accessibility data for all health facilities in the area
        accessibility_data = AccessibilityData.objects.filter(
            health_facility__district=district,
            health_facility__sector=sector
        )
        
        # Get disease incidents
        disease_incidents = DiseaseIncident.objects.filter(
            health_facility__district=district,
            health_facility__sector=sector
        )
        
        # Get resource allocations
        resource_allocations = ResourceAllocation.objects.filter(
            health_facility__district=district,
            health_facility__sector=sector
        )
        
        # Calculate aggregated statistics
        total_facility_capacity = health_facilities.aggregate(
            total_capacity=Sum('capacity')
        )['total_capacity'] or 0
        
        avg_travel_time = accessibility_data.aggregate(
            avg_time=Avg('avg_travel_time')
        )['avg_time'] or 0
        
        # Prepare the response data
        response_data = {
            'district': district,
            'sector': sector,
            'population_data': PopulationDataSerializer(population_data).data if population_data else None,
            'health_facilities': {
                'total_count': health_facilities.count(),
                'total_capacity': total_facility_capacity,
                'grouped_by_type': {
                    facility_type: HealthFacilitySerializer(facilities, many=True).data
                    for facility_type, facilities in grouped_health_facilities.items()
                }
            },
            'accessibility_metrics': {
                'average_travel_time': round(avg_travel_time, 2),
                'detailed_data': AccessibilityDataSerializer(accessibility_data, many=True).data
            },
            'disease_incidents': {
                'total_count': disease_incidents.count(),
                'incidents': DiseaseIncidentSerializer(disease_incidents, many=True).data
            },
            'resource_allocations': {
                'total_count': resource_allocations.count(),
                'allocations': ResourceAllocationSerializer(resource_allocations, many=True).data
            }
        }
        
        # Print the response data to the terminal
        print(response_data)
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {"error": f"An error occurred: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )





















# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_district_sector_data(request):
#     """
#     Get all related information for a specific district and sector.
    
#     Required query parameters:
#     - district: District name
#     - sector: Sector name
#     """
#     district = request.query_params.get('district')
#     sector = request.query_params.get('sector')
    
#     if not district or not sector:
#         return Response(
#             {"error": "Both district and sector parameters are required"},
#             status=status.HTTP_400_BAD_REQUEST
#         )
    
#     try:
#         # Get population data
#         population_data = PopulationData.objects.filter(
#             district=district,
#             sector=sector
#         ).first()
        
#         # Get health facilities
#         health_facilities = HealthFacility.objects.filter(
#             district=district,
#             sector=sector
#         )
        
#         # Get accessibility data for all health facilities in the area
#         accessibility_data = AccessibilityData.objects.filter(
#             health_facility__district=district,
#             health_facility__sector=sector
#         )
        
#         # Get disease incidents
#         disease_incidents = DiseaseIncident.objects.filter(
#             health_facility__district=district,
#             health_facility__sector=sector
#         )
        
#         # Get resource allocations
#         resource_allocations = ResourceAllocation.objects.filter(
#             health_facility__district=district,
#             health_facility__sector=sector
#         )
        
#         # Calculate aggregated statistics
#         total_facility_capacity = health_facilities.aggregate(
#             total_capacity=Sum('capacity')
#         )['total_capacity'] or 0
        
#         avg_travel_time = accessibility_data.aggregate(
#             avg_time=Avg('avg_travel_time')
#         )['avg_time'] or 0
        
#         # Prepare the response data
#         response_data = {
#             'district': district,
#             'sector': sector,
#             'population_data': PopulationDataSerializer(population_data).data if population_data else None,
#             'health_facilities': {
#                 'total_count': health_facilities.count(),
#                 'total_capacity': total_facility_capacity,
#                 'facilities': HealthFacilitySerializer(health_facilities, many=True).data
#             },
#             'accessibility_metrics': {
#                 'average_travel_time': round(avg_travel_time, 2),
#                 'detailed_data': AccessibilityDataSerializer(accessibility_data, many=True).data
#             },
#             'disease_incidents': {
#                 'total_count': disease_incidents.count(),
#                 'incidents': DiseaseIncidentSerializer(disease_incidents, many=True).data
#             },
#             'resource_allocations': {
#                 'total_count': resource_allocations.count(),
#                 'allocations': ResourceAllocationSerializer(resource_allocations, many=True).data
#             }
#         }
        
#         # Print the response data to the terminal
#         print(response_data)
        
#         return Response(response_data, status=status.HTTP_200_OK)
        
#     except Exception as e:
#         return Response(
#             {"error": f"An error occurred: {str(e)}"},
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR
#         )















  
        
        
        
    