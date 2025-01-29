# views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import HealthFacility
from .serializers import HealthFacilitySerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_facility(request):
    serializer = HealthFacilitySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_facilities(request):
    facilities = HealthFacility.objects.all()
    serializer = HealthFacilitySerializer(facilities, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@permission_classes([IsAuthenticated])
def get_facility_by_id(request, pk):
    facility = get_object_or_404(HealthFacility, pk=pk)
    serializer = HealthFacilitySerializer(facility)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_facility_by_name(request, name):
    facilities = HealthFacility.objects.filter(name__icontains=name)
    serializer = HealthFacilitySerializer(facilities, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_facilities_by_district(request, district):
    facilities = HealthFacility.objects.filter(district__iexact=district)
    serializer = HealthFacilitySerializer(facilities, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_facilities_by_sector(request, sector):
    facilities = HealthFacility.objects.filter(sector__iexact=sector)
    serializer = HealthFacilitySerializer(facilities, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_facilities_by_status(request, status):
    facilities = HealthFacility.objects.filter(status__iexact=status)
    serializer = HealthFacilitySerializer(facilities, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_facility(request, pk):
    facility = get_object_or_404(HealthFacility, pk=pk)
    serializer = HealthFacilitySerializer(facility, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_facility(request, pk):
    facility = get_object_or_404(HealthFacility, pk=pk)
    facility.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)