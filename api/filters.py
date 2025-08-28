import django_filters
from api.models import Product, Order
from rest_framework import filters


class InStockFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt=0)

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            "name":["exact","contains"],
            "price":["exact","gt","lt","range"]
        }

class OrderFilter(django_filters.FilterSet):
    order_created = django_filters.DateFilter(field_name='order_created', lookup_expr='date')
    class Meta:
        model = Order
        fields = {
            "status":["exact"],
            "order_created":["exact","gt","lt"]
        }