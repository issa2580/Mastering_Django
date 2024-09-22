from django.contrib import admin
from . import models

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone', 'birth_date', 'membership',]
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    list_per_page = 10


admin.site.register(models.Collection)
admin.site.register(models.Product)
admin.site.register(models.Promotion)
