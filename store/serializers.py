from decimal import Decimal

from rest_framework import serializers

from .models import Collection, Product

# Creating serailiers

class CollectionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']
        
    products_count = serializers.IntegerField(read_only=True)
    
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)

class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = ['id', 'slug', 'title', 'description', 'unit_price', 'price_with_tax', 'inventory', 'collection']
    
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # unit_price = serializers.DecimalField(max_digits=6, decimal_places=2) 
    
    # Cutom serializer field
    price_with_tax = serializers.SerializerMethodField(method_name= 'calculate_price')
    
    # inventory = serializers.IntegerField()
    # last_update = serializers.DateTimeField()
    
    # Create serializer relationship for id
    # collection = serializers.PrimaryKeyRelatedField(queryset=Collection.objects.all())
    
    # Create serializer relationship for string
    # collection = serializers.StringRelatedField()
    
    # Serialize relationship for class
    # collection = CollectionSerializer()
    
    # Create serializer relationship for Hyperlinked
    # collection = serializers.HyperlinkedRelatedField(queryset=Collection.objects.all(), view_name='collection-detail')
    
    def calculate_price(self, product:Product):
        return product.unit_price * Decimal(1.1)
    