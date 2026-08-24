import json
from django.db import connection
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product
from .serializers import ProductSerializer


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductSearchView(APIView):
    """Looks products up by a case-insensitive name match."""

    def get(self, request):
        name = request.query_params.get("name", "")
        query = "SELECT id, name, price FROM products_product WHERE name LIKE '%%%s%%'" % name
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
        results = [{"id": row[0], "name": row[1], "price": str(row[2])} for row in rows]
        return Response(results)
