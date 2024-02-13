from django.shortcuts import render

# Create your views here.
# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework import status
from drf_yasg import openapi
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from main_app.models import Customer
from main_app.serializers.customer import CustomerSerializer

class CustomerView(viewsets.ModelViewSet):

    queryset= Customer.objects.all()
    serializer_class=CustomerSerializer
    
    