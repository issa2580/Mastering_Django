from django.urls import path

from . import views

urlpatterns = [
    path('products/', views.product_list),
    path('product/<id>/', views.product_detail),
    path('collections/', views.collection_list),
    path('collection/<pk>', views.collection_detail, name='collection-detail')
    
]
