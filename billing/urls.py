from django.urls import path

from .views import BillingListCreateView, BillingRetrieveUpdateDestroyView

urlpatterns = [
    path("", BillingListCreateView.as_view(), name="billing-list"),
    path("<int:pk>/", BillingRetrieveUpdateDestroyView.as_view(), name="billing-detail"),
]
