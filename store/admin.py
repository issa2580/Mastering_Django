from django.contrib import admin
from django.db.models import Count
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from . import models


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone', 'birth_date', 'membership',]
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    list_per_page = 10
    
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    # autocomplete_fields = ['featured_product']
    list_display = ['title', 'products_count']
    ordering = ['title']
    
    # @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({'collection__id': str(collection.id)})
        )
        return format_html('<a href="{}">{} Products</a>', url, collection.products_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count('product'))

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory', 'last_update', 'collection_title']
    list_editable = ['unit_price']
    list_select_related = ['collection']
    list_per_page = 15
    
    def collection_title(self, product):
        return product.collection.title

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'payment_status', 'customer']
    
# @admin.register(models.Cart)
# class CartAdmin(admin.ModelAdmin):
#     list_display = ['id', 'created_at']
    
# @admin.register(models.CartItem)
# class CartItemAdmin(admin.ModelAdmin):
#     list_display = ['product', 'quantity']
    
#     def get_queryset(self, request:HttpRequest) -> QuerySet:
#         return super().get_queryset(request).select_related('product')
