
from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from django.http import JsonResponse
from .models import Product, Order
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Max
from rest_framework import generics
from rest_framework.permissions import ( IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
    AllowAny)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters, viewsets
from api.filters import ProductFilter, InStockFilterBackend
from rest_framework.pagination import PageNumberPagination


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [filters.SearchFilter,filters.OrderingFilter,InStockFilterBackend]
    search_fields = ['name','description']
    ordering_fields = ['name', 'price',"stock"]
    filterset_fields = ['name', 'price']
    pagination_class = PageNumberPagination
    pagination_class.page_size = 2
    pagination_class.page_size_query_param = "size"
    pagination_class.max_page_size = 5

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