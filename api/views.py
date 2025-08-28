
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import InStockFilterBackend, OrderFilter, ProductFilter
from api.serializers import (OrderSerializer, ProductInfoSerializer,
                             ProductSerializer, OrderCreateSerializer, UserSerializer)

from .models import Order, Product, User

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
import time


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [filters.SearchFilter,filters.OrderingFilter,InStockFilterBackend]
    search_fields = ['name','description']
    ordering_fields = ['name', 'price',"stock"]
    filterset_fields = ['name', 'price']
    # pagination_class = PageNumberPagination
    pagination_class = None
    # pagination_class.page_size = 2
    # pagination_class.page_size_query_param = "size"
    # pagination_class.max_page_size = 5

    @method_decorator(cache_page(60 * 15, key_prefix='product_list') )
    def list(self, request, *args, **kwargs):
        return super().list(request ,args, **kwargs)
    
    def get_queryset(self):
        time.sleep(2)
        return super().get_queryset()

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ["PUT","PATCH","DELETE"]:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

class ProductInfoAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self,request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
            "products":products,
            "count":len(products),
            "max_price": products.aggregate(max_price=Max('price'))["max_price"]
        })
        return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items','items__product').all()
    serializer_class = OrderSerializer
    pagination_class = None
    filterset_class = OrderFilter
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ["create","update"]:
            return OrderCreateSerializer
        return super().get_serializer_class()
    
    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs


class UserListApiView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = None

    # @action(detail=False, methods=['get'], permission_classes = [IsAuthenticated],url_path="user-orders")
    # def my_orders(self,request):
    #     orders = self.get_queryset().filter(user=request.user)
    #     serializer = self.get_serializer(orders, many=True)
    #     return Response(serializer.data)





# class OrderListAPIView(generics.ListCreateAPIView):
#     queryset =  Order.objects.prefetch_related('items','items__product').all().order_by("order_id")
#     serializer_class = OrderSerializer
#     pagination_class = None

# class UserOrderListAPIView(generics.ListAPIView):
#     queryset =  Order.objects.prefetch_related('items','items__product').all()
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         qs = super().get_queryset()
#         return qs.filter(user=user)


    



# @api_view(['GET'])
# def product_list(response):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products,many=True)
#     return Response(
#         data=serializer.data,
#         status=status.HTTP_200_OK
#     )

# @api_view(['GET'])
# def product_detail(response,pk):
#     product = get_object_or_404(Product,pk=pk)
#     serializer = ProductSerializer(product)
#     return Response(serializer.data,status=status.HTTP_200_OK)

# @api_view(['GET'])
# def product_info(request):
#     products = Product.objects.all()
#     serializer = ProductInfoSerializer({
#         "products":products,
#         "count": len(products),
#         "max_price": products.aggregate(max_price=Max('price'))["max_price"]
#     })
#     return Response(serializer.data,status=status.HTTP_200_OK)