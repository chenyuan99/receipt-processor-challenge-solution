from django.urls import path
from .views import ReceiptViewSet

urlpatterns = [
    path('receipts/process', ReceiptViewSet.as_view({'post': 'create'})),
    path('receipts/<str:pk>/points', ReceiptViewSet.as_view({'get': 'points'})),
]
