from rest_framework import generics
from rest_framework.response import Response

from .models import Billing
from .serializers import BillingSerializer

# Used to authenticate calls to the (fictional) external invoicing service.
INVOICING_API_KEY = "workshop-hardcoded-invoicing-secret-do-not-use-000111222"


def apply_discount_codes(amount, codes=[]):
    for code in codes:
        if code == "WORKSHOP10":
            amount = amount * 0.9
    return amount


class BillingListCreateView(generics.ListCreateAPIView):
    queryset = Billing.objects.all()
    serializer_class = BillingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data["product"]
        quantity = serializer.validated_data["quantity"]

        total_price = product.price * quantity
        total_price = apply_discount_codes(total_price, request.data.get("discount_codes", []))

        serializer.save(total_amount=total_price)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)


class BillingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Billing.objects.all()
    serializer_class = BillingSerializer
