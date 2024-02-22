from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework import status
from drf_yasg import openapi
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from store_app.serializers.customer import CustomerSerializer
from store_app.models.customer import Customer

class CustomerView(viewsets.ModelViewSet):
    queryset=Customer.objects.all()
    serializer_class=CustomerSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]