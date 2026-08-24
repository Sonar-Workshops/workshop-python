from django.urls import path

from .views import CustomerListCreateView, CustomerRetrieveUpdateDestroyView

urlpatterns = [
    path("", CustomerListCreateView.as_view(), name="customer-list"),
    path("<int:pk>/", CustomerRetrieveUpdateDestroyView.as_view(), name="customer-detail"),
]
