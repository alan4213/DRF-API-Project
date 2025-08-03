from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Customer
        fields = ['id', 'name', 'username', 'email', 'phone', 'address', 'created_at']
        read_only_fields = ['id', 'created_at']
