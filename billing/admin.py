from django.contrib import admin
from .models import Customer, Product, BillingData

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(BillingData)