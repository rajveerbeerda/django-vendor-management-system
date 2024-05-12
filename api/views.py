from datetime import datetime
from django.shortcuts import render
from rest_framework import generics, status, views
from .serializers import (
    VendorSerializer,
    PurchaseOrderSerializer,
    HistoricalPerformanceSerializer,
)
from .models import VendorModel, PurchaseOrderModel, HistoricalPerformanceModel
from rest_framework.response import Response
from django.utils import timezone


# Create your views here.
class Vendor(generics.GenericAPIView):
    serializer_class = VendorSerializer
    historical_performance_serializer_class = HistoricalPerformanceSerializer
    queryset = VendorModel.objects.all()

    def get(self, request):
        vendors = VendorModel.objects.all()
        vendors_count = vendors.count()
        serializer = self.serializer_class(vendors, many=True)
        return Response(
            {
                "count": vendors_count,
                "items": serializer.data,
            }
        )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            historical_performance_serializer = (
                self.historical_performance_serializer_class(
                    data={
                        "vendor": serializer.data.get("id"),
                        "on_time_delivery_rate": serializer.data.get(
                            "on_time_delivery_rate"
                        ),
                        "quality_rating_avg": serializer.data.get("quality_rating_avg"),
                        "average_response_time": serializer.data.get(
                            "average_response_time"
                        ),
                        "fulfillment_rate": serializer.data.get("fulfillment_rate"),
                    }
                )
            )
            if historical_performance_serializer.is_valid():
                historical_performance_serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"status": "fail", "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


class VendorDetail(generics.GenericAPIView):
    queryset = VendorModel.objects.all()
    serializer_class = VendorSerializer
    historical_performance_serializer_class = HistoricalPerformanceSerializer

    def get_vendor(self, pk):
        try:
            return VendorModel.objects.get(pk=pk)
        except:
            return None

    def get_historical_performance(self, pk):
        try:
            return HistoricalPerformanceModel.objects.filter(vendor=pk).first()
        except:
            return None

    def get(self, request, pk):
        vendor = self.get_vendor(pk=pk)
        if vendor == None:
            return Response(
                {"status": "fail", "message": f"Vendor with Id: {pk} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.serializer_class(vendor)
        return Response(serializer.data)

    def put(self, request, pk):
        vendor = self.get_vendor(pk)
        if vendor == None:
            return Response(
                {"status": "fail", "message": f"Vendor with Id: {pk} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.serializer_class(vendor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            historical_performance = self.get_historical_performance(pk=pk)
            historical_performance_data = {
                "on_time_delivery_rate": serializer.data.get("on_time_delivery_rate"),
                "quality_rating_avg": serializer.data.get("quality_rating_avg"),
                "average_response_time": serializer.data.get("average_response_time"),
                "fulfillment_rate": serializer.data.get("fulfillment_rate"),
            }
            historical_performance_serializer = (
                self.historical_performance_serializer_class(
                    historical_performance,
                    data=historical_performance_data,
                    partial=True,
                )
            )
            if historical_performance_serializer.is_valid():
                historical_performance_serializer.save()

            return Response(serializer.data)
        return Response(
            {"status": "fail", "message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk):
        vendor = self.get_vendor(pk)
        if vendor == None:
            return Response(
                {"status": "fail", "message": f"Vendor with Id: {pk} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VendorPerformanceEvaluation(generics.GenericAPIView):
    serializer_class = HistoricalPerformanceSerializer
    queryset = HistoricalPerformanceModel.objects.all()

    def get_historical_performance(self, pk):
        try:
            return HistoricalPerformanceModel.objects.filter(vendor=pk)
        except:
            return None

    def get(self, request, pk):
        historical_performance = self.get_historical_performance(pk=pk)
        if historical_performance == None:
            return Response(
                {
                    "status": "fail",
                    "message": f"Historical Performance with Vendor Id: {pk} not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.serializer_class(historical_performance, many=True)
        return Response(serializer.data)


class PurchaseOrder(generics.GenericAPIView):
    serializer_class = PurchaseOrderSerializer
    queryset = PurchaseOrderModel.objects.all()

    def get(self, request):
        purchase_orders = PurchaseOrderModel.objects.all()
        purchase_orders_count = purchase_orders.count()
        serializer = self.serializer_class(purchase_orders, many=True)
        return Response(
            {
                "count": purchase_orders_count,
                "items": serializer.data,
            }
        )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"status": "fail", "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


class PurchaseOrderDetail(generics.GenericAPIView):
    queryset = PurchaseOrderModel.objects.all()
    serializer_class = PurchaseOrderSerializer
    vendor_serializer_class = VendorSerializer
    historical_performance_serializer_class = HistoricalPerformanceSerializer

    def get_purchase_order(self, pk):
        try:
            return PurchaseOrderModel.objects.get(pk=pk)
        except:
            return None

    def get_vendor(self, pk):
        try:
            return VendorModel.objects.get(pk=pk)
        except:
            return None

    def get_historical_performance(self, pk):
        try:
            return HistoricalPerformanceModel.objects.filter(vendor=pk).first()
        except:
            return None

    def get(self, request, pk):
        purchase_order = self.get_purchase_order(pk=pk)
        if purchase_order == None:
            return Response(
                {
                    "status": "fail",
                    "message": f"Purchase Order with Id: {pk} not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.serializer_class(purchase_order)
        return Response(serializer.data)

    def put(self, request, pk):
        purchase_order = self.get_purchase_order(pk)
        if purchase_order == None:
            return Response(
                {
                    "status": "fail",
                    "message": f"Purchase Order with Id: {pk} not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.serializer_class(
            purchase_order, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()

            vendor_data = {}
            vendor = self.get_vendor(pk=purchase_order.vendor.id)
            vendor_total_pos_count = PurchaseOrderModel.objects.filter(
                vendor=purchase_order.vendor
            ).count()
            vendor_completed_pos_count = PurchaseOrderModel.objects.filter(
                vendor=purchase_order.vendor, status="completed"
            ).count()

            if (
                request.data.get("status") == "completed"
                and purchase_order.delivery_date >= timezone.now()
            ):
                vendor_data["on_time_delivery_rate"] = vendor.on_time_delivery_rate + (
                    1 / vendor_total_pos_count
                )

            if request.data.get("quality_rating"):
                vendor_data["quality_rating_avg"] = (
                    vendor.quality_rating_avg + request.data.get("quality_rating")
                ) / 2

            if request.data.get("acknowledgment_date"):
                response_time = (
                    purchase_order.issue_date - request.data.get("acknowledgment_date")
                ).days
                vendor_data["average_response_time"] = (
                    vendor.average_response_time + response_time
                ) / 2

            vendor_data["fulfillment_rate"] = (
                vendor_completed_pos_count / vendor_total_pos_count
            )
            vendor_serializer = self.vendor_serializer_class(
                vendor, data=vendor_data, partial=True
            )
            if vendor_serializer.is_valid():
                vendor_serializer.save()

            historical_performance = self.get_historical_performance(pk=pk)
            historical_performance_data = {
                "on_time_delivery_rate": vendor_data.get("on_time_delivery_rate"),
                "quality_rating_avg": vendor_data.get("quality_rating_avg"),
                "average_response_time": vendor_data.get("average_response_time"),
                "fulfillment_rate": vendor_data.get("fulfillment_rate"),
            }
            historical_performance_serializer = (
                self.historical_performance_serializer_class(
                    historical_performance,
                    data=historical_performance_data,
                    partial=True,
                )
            )
            if historical_performance_serializer.is_valid():
                historical_performance_serializer.save()

            return Response(serializer.data)
        return Response(
            {"status": "fail", "message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk):
        purchase_order = self.get_purchase_order(pk)
        if purchase_order == None:
            return Response(
                {
                    "status": "fail",
                    "message": f"Purchase Order with Id: {pk} not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        purchase_order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AcknowledgePurchaseOrder(views.APIView):
    def get_purchase_order(self, pk):
        try:
            return PurchaseOrderModel.objects.get(pk=pk)
        except:
            return None

    def get_vendor(self, pk):
        try:
            return VendorModel.objects.get(pk=pk)
        except:
            return None

    def put(self, request, pk):
        purchase_order = self.get_purchase_order(pk)
        if purchase_order == None:
            return Response(
                {
                    "status": "fail",
                    "message": f"Purchase Order with Id: {pk} not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()

        response_time = (
            purchase_order.acknowledgment_date - purchase_order.issue_date
        ).days

        vendor = self.get_vendor(pk=purchase_order.vendor.id)
        vendor.average_response_time = (
            vendor.average_response_time + response_time
        ) / 2
        vendor.save()

        return Response({"status": "success"}, status=status.HTTP_200_OK)
