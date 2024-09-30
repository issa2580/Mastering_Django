from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .filters import ProductFilter
from .models import Collection, Product
from .pagination import DefaultPagination
from .serializers import CollectionSerializer, ProductSerializer


# Creating ViewSets
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        if product.orderitems.count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item'}, status=405)
        product.delete()
        return Response(status=204)
    
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('product')).all()
    serializer_class = CollectionSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        collection = self.get_object()
        if collection.product_set.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it contains products'}, status=405)
        collection.delete()
        return Response(status=204)


# Create Generic API View
# class ProductList(ListCreateAPIView):
#     queryset = Product.objects.select_related('collection').all()
#     serializer_class = ProductSerializer
    
#     def get_serializer_context(self):
#         return {'request': self.request}
    
# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
    
#     def delete(self, request, *args, **kwargs):
#         product = self.get_object()
#         if product.orderitems.count() > 0:
#             return Response({'error': 'Product cannot be deleted because it is associated with an order item'}, status=405)
#         product.delete()
#         return Response(status=204)
    
# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('product')).all()
#     serializer_class = CollectionSerializer
    
#     def get_serializer_context(self):
#         return {'request': self.request}
    
# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('product')).all()
#     serializer_class = CollectionSerializer
    
#     def delete(self, request, *args, **kwargs):
#         collection = self.get_object()
#         if collection.product_set.count() > 0:
#             return Response({'error': 'Collection cannot be deleted because it contains products'}, status=405)
#         collection.delete()
#         return Response(status=204)

# Create Class based view
# class ProductList(APIView):
#     def get(self, request):
#         queryset = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(queryset, many=True, context={ 'request': request})
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('ok')
    
# class ProductDetail(APIView):
#     def get(self, request, id):
#         product = Product.objects.get(pk=id)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
    
#     def put(self, request, id):
#         product = Product.objects.get(pk=id)
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
    
#     def delete(self, request, id):
#         product = Product.objects.get(pk=id)
#         product.delete()
#         return Response(status=204)
    

# @api_view(['GET', 'POST'])
# def collection_list(request):
#     if request.method == 'GET':
#         queryset = Collection.objects.annotate(products_count=Count('product')).all()
#         serializer = CollectionSerializer(queryset, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=201)

# Creating API View
# @api_view(['GET', 'POST'])
# def product_list(request):
#     if request.method == 'GET':
#         queryset = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(queryset, many=True, context={ 'request': request})
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('ok')

# @api_view(['GET', 'PUT', 'DELETE'])
# def product_detail(request, id):
#     product = Product.objects.get(pk=id)
#     if request.method == 'GET':
#         try:
#             # Get product detail without try and catch
#             # product = get_object_or_404(Product, pk=id)
#             serializer = ProductSerializer(product)
#             return Response(serializer.data)
#         except Product.DoesNotExist:
#             return Response(status=404)
#     elif request.method == 'PUT':
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=201)
#     elif request.method == 'DELETE':
#         if product.orderitems.count() > 0:
#             return Response({'error': 'Product cannot be deleted because it is associated with an order item'}, status=405)
#         product.adelete()
#         return Response(status=204)

# @api_view(['GET', 'PUT', 'DELETE']) 
# def collection_detail(request, pk):
#     collection = get_object_or_404(Collection.objects.annotate(products_count=Count('product')), pk=pk)
#     if request.method == 'GET':
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = CollectionSerializer(collection, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if collection.product_set.count() > 0:
#             return Response({'error': 'Collection cannot be deleted because it contains products'}, status=405)
#         collection.delete()
#         return Response(status=204)
