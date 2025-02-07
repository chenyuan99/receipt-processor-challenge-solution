from rest_framework import serializers
from .models import Receipt, ReceiptItem

class ReceiptItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiptItem
        fields = ['short_description', 'price']

class ReceiptSerializer(serializers.ModelSerializer):
    items = ReceiptItemSerializer(many=True)

    class Meta:
        model = Receipt
        fields = ['retailer', 'purchase_date', 'purchase_time', 'total', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        receipt = Receipt.objects.create(**validated_data)
        
        # Calculate points
        points = 0
        
        # Rule 1: One point for every alphanumeric character in the retailer name
        points += sum(c.isalnum() for c in receipt.retailer)
        
        # Rule 2: 50 points if the total is a round dollar amount with no cents
        if float(receipt.total) == int(float(receipt.total)):
            points += 50
            
        # Rule 3: 25 points if the total is a multiple of 0.25
        if float(receipt.total) % 0.25 == 0:
            points += 25
            
        # Rule 4: 5 points for every two items on the receipt
        points += (len(items_data) // 2) * 5
        
        # Rule 5: If the trimmed length of the item description is a multiple of 3
        # multiply the price by 0.2 and round up to the nearest integer
        for item_data in items_data:
            description = item_data['short_description'].strip()
            if len(description) % 3 == 0:
                points += int(float(item_data['price']) * 0.2 + 0.99)
            ReceiptItem.objects.create(receipt=receipt, **item_data)
            
        # Rule 6: 6 points if the day in the purchase date is odd
        if receipt.purchase_date.day % 2 == 1:
            points += 6
            
        # Rule 7: 10 points if the time of purchase is after 2:00pm and before 4:00pm
        if 14 <= receipt.purchase_time.hour < 16:
            points += 10
            
        receipt.points = points
        receipt.save()
        
        return receipt
