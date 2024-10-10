from django.urls import path, include

urlpatterns = [
    path('customers/', include('customers.urls')),
    path('products/', include('products.urls')),
    path('billing/', include('billing.urls')),
]