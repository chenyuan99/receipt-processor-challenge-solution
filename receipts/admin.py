from django.contrib import admin
from .models import Receipt, ReceiptItem

# Register your models here.

@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('id', 'retailer', 'purchase_date', 'purchase_time', 'total', 'points', 'created_at')
    list_filter = ('purchase_date', 'created_at')
    search_fields = ('retailer', 'id')
    readonly_fields = ('points', 'created_at')

@admin.register(ReceiptItem)
class ReceiptItemAdmin(admin.ModelAdmin):
    list_display = ('receipt', 'short_description', 'price')
    list_filter = ('receipt__purchase_date',)
    search_fields = ('short_description', 'receipt__retailer')
    raw_id_fields = ('receipt',)
