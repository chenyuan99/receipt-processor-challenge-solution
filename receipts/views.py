from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
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
            receipt = Receipt.objects.get(id=pk)
            return Response({'points': receipt.points}, status=status.HTTP_200_OK)
        except Receipt.DoesNotExist:
            return Response({'error': 'Receipt not found'}, status=status.HTTP_404_NOT_FOUND)
