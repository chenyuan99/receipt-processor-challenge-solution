from django.db import models
import uuid

# Create your models here.

class Receipt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    retailer = models.CharField(max_length=255)
    purchase_date = models.DateField()
    purchase_time = models.TimeField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class ReceiptItem(models.Model):
    receipt = models.ForeignKey(Receipt, related_name='items', on_delete=models.CASCADE)
    short_description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
