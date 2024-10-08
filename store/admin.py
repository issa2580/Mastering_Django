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
    list_display = ['first_name', 'last_name', 'phone', 'membership']
    list_editable = ['membership']
    list_per_page = 10
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    list_select_related = ['user']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    
    @admin.display(ordering='order_count')
    def orders(self, customer):
        url = (
            reverse('admin:store_order_changelist')
            + '?'
            + urlencode({'customer__id': str(customer.id)})
        )
        return format_html('<a href="{}">{}</a>', url, customer.order_count)
    
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    ordering = ['title']
    
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

