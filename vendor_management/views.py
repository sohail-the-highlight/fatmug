from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Count, F
from datetime import datetime
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    @action(detail=True, methods=['get'])
    def performance(self, request, pk=None):
        vendor = self.get_object()
        
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        total_completed_pos = completed_pos.count()
        
        # Calculate On-Time Delivery Rate
        on_time_deliveries = completed_pos.filter(delivery_date__lte=F('acknowledgment_date')).count()
        on_time_delivery_rate = (on_time_deliveries * 100.0) / total_completed_pos if total_completed_pos > 0 else 0.0
        
        # Calculate Quality Rating Average
        quality_rating_avg = completed_pos.aggregate(avg_quality=Avg('quality_rating'))['avg_quality'] or 0.0
        
        # Calculate Average Response Time
        avg_response_time = completed_pos.exclude(acknowledgment_date=None).aggregate(avg_response=Avg(F('acknowledgment_date') - F('issue_date')))['avg_response'] or 0.0
        
        # Calculate Fulfillment Rate
        fulfilled_pos = completed_pos.filter(issues=None)
        fulfillment_rate = (fulfilled_pos.count() * 100.0) / total_completed_pos if total_completed_pos > 0 else 0.0
        
        vendor.on_time_delivery_rate = on_time_delivery_rate
        vendor.quality_rating_avg = quality_rating_avg
        vendor.average_response_time = avg_response_time
        vendor.fulfillment_rate = fulfillment_rate
        vendor.save()
        
        return Response({
            'on_time_delivery_rate': on_time_delivery_rate,
            'quality_rating_avg': quality_rating_avg,
            'average_response_time': avg_response_time,
            'fulfillment_rate': fulfillment_rate
        })

    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        po = self.get_object()
        if po.vendor:
            po.vendor.average_response_time = ((po.vendor.average_response_time * po.vendor.purchaseorder_set.count()) + (po.acknowledgment_date - po.issue_date).seconds) / (po.vendor.purchaseorder_set.count() + 1)
            po.vendor.save()
        po.acknowledgment_date = datetime.now()
        po.save()
        serializer = self.get_serializer(po)
        return Response(serializer.data)

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
