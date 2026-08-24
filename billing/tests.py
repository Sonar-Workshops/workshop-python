from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from customers.models import Customer
from products.models import Product
from .models import Billing
from .serializers import BillingSerializer


class BillingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(
            name="John Doe", email="johndoe@example.com", phone="1234567890", address="1 Main St"
        )
        self.product = Product.objects.create(name="Product 1", price=9.99, description="A product")
        self.billing = Billing.objects.create(
            customer=self.customer, product=self.product, quantity=2, total_amount=19.98
        )

    def test_create_billing(self):
        url = reverse("billing-list")
        data = {
            "customer": self.customer.id,
            "product": self.product.id,
            "quantity": 3,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Billing.objects.count(), 2)

    def test_get_billing(self):
        url = reverse("billing-detail", kwargs={"pk": self.billing.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, BillingSerializer(self.billing).data)

    def test_update_billing(self):
        url = reverse("billing-detail", kwargs={"pk": self.billing.id})
        data = {
            "customer": self.customer.id,
            "product": self.product.id,
            "quantity": 5,
            "total_amount": "49.95",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.billing.refresh_from_db()
        self.assertEqual(self.billing.quantity, 5)

    def test_delete_billing(self):
        url = reverse("billing-detail", kwargs={"pk": self.billing.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Billing.objects.count(), 0)
