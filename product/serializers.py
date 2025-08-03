from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'description', 'image', 'priority', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be positive")
        return value
