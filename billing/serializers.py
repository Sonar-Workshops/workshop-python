from rest_framework import serializers
from .models import Customer, Product, BillingData

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class BillingDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingData
        fields = '__all__'