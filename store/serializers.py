from decimal import Decimal

from django.db import transaction
from rest_framework import serializers

from store.signals import order_created

from .models import (Cart, CartItem, Collection, Customer, Order, OrderItem,
                     Product, ProductImage, Review)


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']
        
    products_count = serializers.IntegerField(read_only=True)
    
class ProductImageSerializer(serializers.ModelSerializer):
    
    def create(self, validated_data):
        product_id = self.context['product_id']
        return ProductImage.objects.create(product_id=product_id, **validated_data)
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)
    class Meta:
        model = Product
        fields = ['id', 'slug', 'title', 'description', 'unit_price', 'price_with_tax', 'inventory', 'collection', 'images']
    
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
        fields = ['id', 'product', 'quantity', 'total_price']

class AddCartItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    
    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError('Product not found')
        
        return value
    
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
            
        return self.instance
    
    class Meta:
        fields = ['id', 'product_id', 'quantity']        
        
class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()
    
    def get_total_price(self, cart:Cart):
        return sum([item.product.unit_price * item.quantity for item in cart.items.all()])
    
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']
        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)
    
    
class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']
        
class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']
        
class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'unit_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id', 'customer', 'placed_at', 'payment_status', 'items']
        

class UpdateOrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = ['payment_status']
        
class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    
    def validated_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('Cart not found')
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
                raise serializers.ValidationError('Cart is empty')
        return cart_id
    
    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            
            customer = Customer.objects.get(user_id=self.context['request'].user.id)
            order = Order.objects.create(customer=customer)
            
            cart_items = CartItem.objects.select_related('product').filter(cart_id=cart_id)
            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    unit_price=item.product.unit_price
                )for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)
            
            Cart.objects.filter(pk=cart_id).delete()
            
            order_created.send_robust(self.__class__, order=order)
            
            return order
    
        
        
    