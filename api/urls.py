from django.urls import path
from api.views import (
    Vendor,
    VendorDetail,
    VendorPerformanceEvaluation,
    PurchaseOrder,
    PurchaseOrderDetail,
    AcknowledgePurchaseOrder,
)


urlpatterns = [
    path("vendors/", Vendor.as_view()),
    path("vendors/<str:pk>/", VendorDetail.as_view()),
    path("vendors/<str:pk>/performance", VendorPerformanceEvaluation.as_view()),
    path("purchase_orders/", PurchaseOrder.as_view()),
    path("purchase_orders/<str:pk>/", PurchaseOrderDetail.as_view()),
    path("purchase_orders/<str:pk>/acknowledge", AcknowledgePurchaseOrder.as_view()),
]
