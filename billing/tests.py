from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Customer, Product, BillingData
from .serializers import CustomerSerializer, ProductSerializer, BillingDataSerializer

class CustomerTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer_data = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'phone': '1234567890'
        }
        self.customer = Customer.objects.create(**self.customer_data)

    def test_create_customer(self):
        url = reverse('customer-list')
        response = self.client.post(url, self.customer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 2)

    def test_get_customer(self):
        url = reverse('customer-detail', kwargs={'pk': self.customer.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, CustomerSerializer(self.customer).data)

    def test_update_customer(self):
        url = reverse('customer-detail', kwargs={'pk': self.customer.id})
        updated_data = {
            'name': 'Jane Doe',
            'email': 'janedoe@example.com',
            'phone': '9876543210'
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.name, updated_data['name'])
        self.assertEqual(self.customer.email, updated_data['email'])
        self.assertEqual(self.customer.phone, updated_data['phone'])

    def test_delete_customer(self):
        url = reverse('customer-detail', kwargs={'pk': self.customer.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Customer.objects.count(), 0)

class ProductTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product_data = {
            'name': 'Product 1',
            'price': 9.99
        }
        self.product = Product.objects.create(**self.product_data)

    def test_create_product(self):
        url = reverse('product-list')
        response = self.client.post(url, self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_get_product(self):
        url = reverse('product-detail', kwargs={'pk': self.product.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, ProductSerializer(self.product).data)

    def test_update_product(self):
        url = reverse('product-detail', kwargs={'pk': self.product.id})
        updated_data = {
            'name': 'Product 2',
            'price': 19.99
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, updated_data['name'])
        self.assertEqual(self.product.price, updated_data['price'])

    def test_delete_product(self):
        url = reverse('product-detail', kwargs={'pk': self.product.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

class BillingDataTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(name='John Doe', email='johndoe@example.com', phone='1234567890')
        self.product = Product.objects.create(name='Product 1', price=9.99)
        self.billing_data = {
            'customer': self.customer,
            'product': self.product,
            'quantity': 2,
            'total_amount': 19.98
        }
        self.billing = BillingData.objects.create(**self.billing_data)

    def test_create_billing_data(self):
        url = reverse('billing-list')
        response = self.client.post(url, self.billing_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BillingData.objects.count(), 2)

    def test_get_billing_data(self):
        url = reverse('billing-detail', kwargs={'pk': self.billing.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, BillingDataSerializer(self.billing).data)

    def test_update_billing_data(self):
        url = reverse('billing-detail', kwargs={'pk': self.billing.id})
        updated_data = {
            'quantity': 3,
            'total_amount': 29.97
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.billing.refresh_from_db()
        self.assertEqual(self.billing.quantity, updated_data['quantity'])
        self.assertEqual(self.billing.total_amount, updated_data['total_amount'])

    def test_delete_billing_data(self):
        url = reverse('billing-detail', kwargs={'pk': self.billing.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(BillingData.objects.count(), 0)