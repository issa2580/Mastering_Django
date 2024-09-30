from decimal import Decimal

from rest_framework import serializers

from .models import Cart, CartItem, Collection, Product


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']
        
    products_count = serializers.IntegerField(read_only=True)

class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = ['id', 'slug', 'title', 'description', 'unit_price', 'price_with_tax', 'inventory', 'collection']
    
    price_with_tax = serializers.SerializerMethodField(method_name= 'calculate_price')
    
    def calculate_price(self, product:Product):
        return product.unit_price * Decimal(1.1)
    
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']
    
class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()
    
    def get_total_price(self, cart_item:CartItem):
        return cart_item.product.unit_price * cart_item.quantity
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']
class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()
    
    def get_total_price(self, cart):
        return sum([item.product.unit_price * item.quantity for item in cart.items.all()])
    
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']
        
        
    