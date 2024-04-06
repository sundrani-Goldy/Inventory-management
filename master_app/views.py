from django.shortcuts import render

# Create your views here.
from master_app.models import Store
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from master_app.serializers import StoreSerializer

class StoreView(ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer