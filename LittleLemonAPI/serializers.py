from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, MenuItem, Cart, Order

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title", "slug"]

class MenuItemSerializer(serializers.ModelSerializer):
    # category = CategorySerializer(read_only=True)
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category']

class CartSerializer(serializers.ModelSerializer):
    
    def create(self, validated_data):
        menuitem = validated_data.get('menuitem')

        # Calculate the price based on unit_price and quantity
        unit_price =  menuitem.price
        quantity = validated_data.get('quantity')
        price = unit_price * quantity

        # Access the current authenticated user from the context
        user = self.context['request'].user

        validated_data['user'] = user
        validated_data['unit_price'] = unit_price
        validated_data['price'] = price

        # Create and return the Cart object with the updated data
        cart = Cart.objects.create(**validated_data)
        return cart
    
    class Meta:
        model = Cart
        fields = ['id', 'menuitem', 'quantity', 'user', 'price', 'unit_price']
        extra_kwargs = {"price": {"read_only": True}, "unit_price": {"read_only": True}, "user": {"read_only": True}}

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "user", "delivery_crew", "status", "total", "date"]
        extra_kwargs = {"delivery_crew": {"read_only": True}, "status": {"read_only": True}}