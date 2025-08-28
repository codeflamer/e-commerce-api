from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path("products/",views.ProductListCreateAPIView.as_view(),name="user-products"),
    path("products/info/",views.ProductInfoAPIView.as_view()),
    path("products/<int:pk>/",views.ProductDetailAPIView.as_view()),
    path("users/",views.UserListApiView.as_view()),
    # path("user-orders/",views.UserOrderListAPIView.as_view(),name="user-orders"),

]

router = DefaultRouter()
router.register("orders",views.OrderViewSet)
urlpatterns = urlpatterns + router.urls
