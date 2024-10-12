from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.contenttypes.admin import GenericTabularInline

from store.admin import ProductAdmin, ProductImageInline
from store.models import Product
from tags.models import Tag, TaggedItem

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name'),
        }),
    )
    
class TagInline(GenericTabularInline):
    # autocomplete_fields = ['tag']
    model = TaggedItem
    
class CustomerProductAdmin(ProductAdmin):
    inlines = [TagInline, ProductImageInline]
    
admin.site.unregister(Product)
admin.site.register(Product, CustomerProductAdmin)
    
