from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
import logging
import os
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import HttpResponseServerError
from rest_framework import status
from store_app.serializers.product import ProductSerializer
from store_app.models.product import Product






class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        product_serializer = ProductSerializer(data=request.data)
        if product_serializer.is_valid():
            product = product_serializer.save()
            return Response(product_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


