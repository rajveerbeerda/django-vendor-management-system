from rest_framework import serializers
from api.models import VendorModel, PurchaseOrderModel, HistoricalPerformanceModel


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorModel
        fields = "__all__"


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderModel
        fields = "__all__"


class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformanceModel
        fields = "__all__"
