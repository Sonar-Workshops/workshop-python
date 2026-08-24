from django.urls import path

from .views import ProductListCreateView, ProductRetrieveUpdateDestroyView, ProductSearchView

urlpatterns = [
    path("", ProductListCreateView.as_view(), name="product-list"),
    path("search/", ProductSearchView.as_view(), name="product-search"),
    path("<int:pk>/", ProductRetrieveUpdateDestroyView.as_view(), name="product-detail"),
]
