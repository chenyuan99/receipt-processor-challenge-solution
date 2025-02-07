from django.db import models
import uuid
from decimal import Decimal
import math

# Create your models here.

class Receipt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    retailer = models.CharField(max_length=255)
    purchase_date = models.DateField()
    purchase_time = models.TimeField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_points(self):
        points = 0
        
        # Rule 1: One point for every alphanumeric character in the retailer name
        retailer_points = sum(c.isalnum() for c in self.retailer)
        points += retailer_points
        print(f"Retailer points: {retailer_points} (for {self.retailer})")
        
        # Rule 2: 50 points if the total is a round dollar amount with no cents
        if self.total % 1 == 0:
            points += 50
            print(f"Round dollar points: 50 (total: {self.total})")
            
        # Rule 3: 25 points if the total is a multiple of 0.25
        if self.total % Decimal('0.25') == 0:
            points += 25
            print(f"Quarter multiple points: 25 (total: {self.total})")
            
        # Rule 4: 5 points for every two items on the receipt
        items_count = self.items.count()
        pair_points = (items_count // 2) * 5
        points += pair_points
        print(f"Item pair points: {pair_points} ({items_count} items)")
        
        # Rule 5: If the trimmed length of the item description is a multiple of 3
        # multiply the price by 0.2 and round up to the nearest integer
        description_points = 0
        for item in self.items.all():
            description = item.short_description.strip()
            if len(description) % 3 == 0:
                item_points = math.ceil(float(item.price) * 0.2)
                description_points += item_points
                print(f"Description points: {item_points} (description: {description}, length: {len(description)}, price: {item.price})")
        points += description_points
            
        # Rule 6: 6 points if the day in the purchase date is odd
        if self.purchase_date.day % 2 == 1:
            points += 6
            print(f"Odd day points: 6 (day: {self.purchase_date.day})")
            
        # Rule 7: 10 points if the time of purchase is after 2:00pm and before 4:00pm
        if 14 <= self.purchase_time.hour < 16:
            points += 10
            print(f"Time range points: 10 (time: {self.purchase_time})")
            
        print(f"Total points: {points}")
        self.points = points
        self.save()
        return points

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class ReceiptItem(models.Model):
    receipt = models.ForeignKey(Receipt, related_name='items', on_delete=models.CASCADE)
    short_description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
