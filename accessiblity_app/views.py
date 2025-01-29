from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import AccessibilityData
from .serializers import AccessibilityDataSerializer
from health_facility_app.models import HealthFacility

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_accessibility_data(request):
    try:
        data = request.data
        health_facility_id = data.get('health_facility_id')

        # Validate health_facility
        try:
            facility = HealthFacility.objects.get(id=health_facility_id)
        except HealthFacility.DoesNotExist:
            return Response({"error": f"Health facility with ID {health_facility_id} does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Set created_by to the current user
        data['created_by'] = request.user.id

        serializer = AccessibilityDataSerializer(data=data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_accessibility_data_by_id(request, pk):
    try:
        data = AccessibilityData.objects.get(id=pk)
        serializer = AccessibilityDataSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except AccessibilityData.DoesNotExist:
        return Response({"error": f"Accessibility data with ID {pk} does not exist."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_accessibility_data(request):
    """
    Retrieve all accessibility records.
    """
    try:
        data = AccessibilityData.objects.all()
        serializer = AccessibilityDataSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_accessibility_data_by_user(request):
    """
    Retrieve all accessibility records created by the logged-in user.
    """
    try:
        user = request.user
        data = AccessibilityData.objects.filter(created_by=user)
        serializer = AccessibilityDataSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_accessibility_data_by_facility(request):
    """
    Retrieve accessibility records based on facility name.
    """
    try:
        facility_name = request.data.get('facility_name')

        # Validate that the facility name is provided
        if not facility_name:
            return Response({"error": "Facility name is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            facility = HealthFacility.objects.get(name__iexact=facility_name)  # Case-insensitive match
        except HealthFacility.DoesNotExist:
            return Response({"error": f"Health facility with name '{facility_name}' does not exist."}, status=status.HTTP_404_NOT_FOUND)

        data = AccessibilityData.objects.filter(health_facility=facility)
        serializer = AccessibilityDataSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_accessibility_data(request, pk):
    try:
        data = AccessibilityData.objects.get(id=pk)

        # Check if the current user is the one who created the data
        if data.created_by != request.user:
            return Response({"error": "You do not have permission to update this record."}, status=status.HTTP_403_FORBIDDEN)

        serializer = AccessibilityDataSerializer(data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except AccessibilityData.DoesNotExist:
        return Response({"error": f"Accessibility data with ID {pk} does not exist."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_accessibility_data(request, pk):
    try:
        data = AccessibilityData.objects.get(id=pk)

        # Check if the current user is the one who created the data
        if data.created_by != request.user:
            return Response({"error": "You do not have permission to delete this record."}, status=status.HTTP_403_FORBIDDEN)

        data.delete()
        return Response({"message": "Accessibility data deleted successfully."}, status=status.HTTP_200_OK)
    except AccessibilityData.DoesNotExist:
        return Response({"error": f"Accessibility data with ID {pk} does not exist."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
