from tenant_app.models import Domain
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
from tenant_app.serializers.domain import DomainSerializer

class DomainView(viewsets.ModelViewSet):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer

    @swagger_auto_schema(auto_schema    =None)
    def retrieve(self, request, *args, **kwargs):
        pass

    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):
        pass

    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs): 
        pass

    @swagger_auto_schema(auto_schema=None)
    def destroy(self, request, *args, **kwargs):
        pass

    @swagger_auto_schema(auto_schema=None)
    def create(self, request, *args, **kwargs):
        pass