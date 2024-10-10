from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Product
from .serializers import ProductSerializer

class ProductTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_product(self):
        url = reverse('product-list')
        data = {
            'name': 'Test Product',
            'price': 9.99,
            'description': 'This is a test product'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, 'Test Product')

    def test_update_product(self):
        product = Product.objects.create(name='Test Product', price=9.99, description='This is a test product')
        url = reverse('product-detail', args=[product.id])
        data = {
            'name': 'Updated Product',
            'price': 19.99,
            'description': 'This is an updated product'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.get().name, 'Updated Product')

    def test_get_product(self):
        product = Product.objects.create(name='Test Product', price=9.99, description='This is a test product')
        url = reverse('product-detail', args=[product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, ProductSerializer(product).data)

    def test_delete_product(self):
        product = Product.objects.create(name='Test Product', price=9.99, description='This is a test product')
        url = reverse('product-detail', args=[product.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)