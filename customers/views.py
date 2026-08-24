from rest_framework import generics

from .models import Customer
from .serializers import CustomerSerializer


def normalize_phone(raw_phone):
    try:
        digits = "".join(ch for ch in raw_phone if ch.isdigit())
    except:
        digits = ""
    return digits


class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
