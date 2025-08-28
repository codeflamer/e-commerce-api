from rest_framework import serializers
from .models import Product,Order, OrderItem, User
from django.db import transaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "is_staff",
            "is_superuser"
        )

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
         model = Product
         exclude = ["id","image"]

    def validate_price(self,value):
        """
        Check that price is greater than 0
        """
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than 0"
            )
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name",required=False)
    product_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        source="product.price", required=False)

    class Meta:
         model = OrderItem
         fields = (
            "product_name",
            "product_price",
            "quantity",
            "item_subtotal"
        )

class OrderCreateSerializer(serializers.ModelSerializer):
    class InstanceOrderItemSerializer(serializers.ModelSerializer):
        class Meta:
            model = OrderItem
            fields = (
                "product",
                "quantity"
            )
    items = InstanceOrderItemSerializer(many=True,required=False)
    order_id = serializers.UUIDField(read_only=True)

    def update(self, instance, validated_data):
        order_items = validated_data.pop("items")
        # instance = super().update(instance, validated_data)
        instance.status = validated_data.get("status",instance.status)
        with transaction.atomic():
            if order_items is not None:
                instance.items.all().delete()

                for order_item in order_items:
                    OrderItem.objects.create(order=instance, **order_item)
        
        return instance

    def create(self,validated_data):
        order_items = validated_data.pop("items")
        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            for order_item in order_items:
                OrderItem.objects.create(order=order, **order_item)
        
        return order

    class Meta:
        model = Order
        fields = (
            "order_id",
            "user",
            "status",
            "items"
        ) 
        read_only_fields = ["user"]

class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(read_only=True)
    items = OrderItemSerializer(many=True)
    total_price = serializers.SerializerMethodField(method_name="total")
    
    def total(self,obj):
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)


    class Meta:
         model = Order
         fields = (
            "order_id",
            "user",
            "order_created",
            "status",
            "items",
            "total_price"
        )

class ProductInfoSerializer(serializers.Serializer):
    """
    get all the products, count of products and max price
    """
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()




