from rest_framework import serializers
from .models import Receipt, ReceiptItem
from datetime import datetime

class ReceiptItemSerializer(serializers.ModelSerializer):
    shortDescription = serializers.CharField(source='short_description')
    
    class Meta:
        model = ReceiptItem
        fields = ['shortDescription', 'price']

class ReceiptSerializer(serializers.ModelSerializer):
    items = ReceiptItemSerializer(many=True)
    purchaseDate = serializers.DateField(source='purchase_date', input_formats=['%Y-%m-%d'])
    purchaseTime = serializers.TimeField(source='purchase_time', input_formats=['%H:%M'])

    class Meta:
        model = Receipt
        fields = ['retailer', 'purchaseDate', 'purchaseTime', 'total', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        receipt = Receipt.objects.create(**validated_data)
        
        for item_data in items_data:
            ReceiptItem.objects.create(receipt=receipt, **item_data)
        
        # Calculate points after all items are created
        receipt.points = receipt.calculate_points()
        receipt.save()
        
        return receipt
