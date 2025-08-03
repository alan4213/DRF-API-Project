from rest_framework import serializers
from .models import Order, OrderItems
from product.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = OrderItems
        fields = ['id', 'product', 'quantity']
    
    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1")
        return value

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_order_status_display', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_status', 'status_display', 'total_price', 'created_at',
            'shipping_name', 'shipping_phone', 'shipping_email',
            'shipping_address', 'shipping_city', 'shipping_state',
            'shipping_pincode', 'order_items'
        ]
        read_only_fields = ['id', 'created_at', 'total_price']
