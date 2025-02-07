from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.utils.encoding import force_str
from uuid import UUID
from .models import Receipt
from .serializers import ReceiptSerializer

# Create your views here.

class ReceiptViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = ReceiptSerializer(data=request.data)
        if serializer.is_valid():
            receipt = serializer.save()
            return Response({'id': str(receipt.id)}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def points(self, request, pk=None):
        try:
            # Validate UUID format
            try:
                uuid_obj = UUID(pk)
            except (AttributeError, ValueError):
                return Response(
                    {'error': 'Invalid receipt ID format'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            receipt = Receipt.objects.get(id=uuid_obj)
            return Response({'points': receipt.points}, status=status.HTTP_200_OK)
        except Receipt.DoesNotExist:
            return Response(
                {'error': 'No receipt found for that ID'}, 
                status=status.HTTP_404_NOT_FOUND
            )
