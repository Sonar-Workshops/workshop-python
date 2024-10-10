from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Customer
from .serializers import CustomerSerializer

class CustomerTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_customer(self):
        url = reverse('customer-list')
        data = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'phone': '1234567890'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        customer = Customer.objects.get(pk=response.data['id'])
        serializer = CustomerSerializer(customer)
        self.assertEqual(response.data, serializer.data)

    def test_get_customer(self):
        customer = Customer.objects.create(
            name='John Doe',
            email='johndoe@example.com',
            phone='1234567890'
        )
        url = reverse('customer-detail', args=[customer.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = CustomerSerializer(customer)
        self.assertEqual(response.data, serializer.data)

    def test_update_customer(self):
        customer = Customer.objects.create(
            name='John Doe',
            email='johndoe@example.com',
            phone='1234567890'
        )
        url = reverse('customer-detail', args=[customer.id])
        data = {
            'name': 'Jane Doe',
            'email': 'janedoe@example.com',
            'phone': '9876543210'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        customer.refresh_from_db()
        self.assertEqual(customer.name, 'Jane Doe')
        self.assertEqual(customer.email, 'janedoe@example.com')
        self.assertEqual(customer.phone, '9876543210')

    def test_delete_customer(self):
        customer = Customer.objects.create(
            name='John Doe',
            email='johndoe@example.com',
            phone='1234567890'
        )
        url = reverse('customer-detail', args=[customer.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Customer.objects.filter(pk=customer.id).exists())