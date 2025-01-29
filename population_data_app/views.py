from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from .models import PopulationData
from .serializers import PopulationDataSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_population(request):
    try:
        serializer = PopulationDataSerializer(data=request.data)
        if serializer.is_valid():
            # Check if population data already exists for this district/sector
            if PopulationData.objects.filter(
                district=request.data['district'],
                sector=request.data['sector']
            ).exists():
                error_message = 'Population data for this district and sector already exists.'
                print(f"Validation Error: {error_message}")
                return Response(
                    {'error': error_message},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Log serializer validation errors
        print(f"Serializer Errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except ValidationError as e:
        # Log validation errors
        print(f"ValidationError: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        # Log unexpected errors
        print(f"Unexpected Error: {str(e)}")
        return Response(
            {'error': f'Failed to create population data: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_population_by_id(request, pk):
    try:
        population = get_object_or_404(PopulationData, pk=pk)
        serializer = PopulationDataSerializer(population)
        return Response(serializer.data)
    except PopulationData.DoesNotExist:
        return Response(
            {'error': f'Population data with ID {pk} not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': f'Failed to retrieve population data: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_populations(request):
    try:
        populations = PopulationData.objects.all().select_related('created_by')
        if not populations.exists():
            return Response(
                {'message': 'No population data found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = PopulationDataSerializer(populations, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': f'Failed to retrieve population data: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_populations_by_user(request):
    try:
        populations = PopulationData.objects.filter(
            created_by=request.user
        ).select_related('created_by')
        
        if not populations.exists():
            return Response(
                {'message': 'No population data found for this user'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        serializer = PopulationDataSerializer(populations, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': f'Failed to retrieve user population data: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_population(request, pk):
    try:
        population = get_object_or_404(PopulationData, pk=pk)
        serializer = PopulationDataSerializer(population, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except PopulationData.DoesNotExist:
        return Response(
            {'error': f'Population data with ID {pk} not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(
            {'error': f'Failed to update population data: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_population(request, pk):
    try:
        population = get_object_or_404(PopulationData, pk=pk)
        population.delete()
        return Response(
            {'message': f'Population data with ID {pk} successfully deleted'},
            status=status.HTTP_204_NO_CONTENT
        )
    except PopulationData.DoesNotExist:
        return Response(
            {'error': f'Population data with ID {pk} not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': f'Failed to delete population data: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_populations_by_district(request, district):
    try:
        populations = PopulationData.objects.filter(
            district__iexact=district
        ).select_related('created_by')
        
        if not populations.exists():
            return Response(
                {'message': f'No population data found for district "{district}"'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        serializer = PopulationDataSerializer(populations, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': f'Failed to retrieve district population data: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_populations_by_sector(request, sector):
    try:
        populations = PopulationData.objects.filter(
            sector__iexact=sector
        ).select_related('created_by')
        
        if not populations.exists():
            return Response(
                {'message': f'No population data found for sector "{sector}"'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        serializer = PopulationDataSerializer(populations, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': f'Failed to retrieve sector population data: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_populations_by_socioeconomic_status(request, status_value):
    try:
        if status_value not in dict(PopulationData.SOCIOECONOMIC_STATUS_CHOICES):
            return Response(
                {'error': f'Invalid socioeconomic status: {status_value}'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        populations = PopulationData.objects.filter(
            socioeconomic_status__iexact=status_value
        ).select_related('created_by')
        
        if not populations.exists():
            return Response(
                {'message': f'No population data found for socioeconomic status "{status_value}"'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        serializer = PopulationDataSerializer(populations, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': f'Failed to retrieve socioeconomic status population data: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )