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
from store_app.serializers.order import *
from store_app.models.order import *



class OrderView(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]

    def list(self, request, *args, **kwargs):
        serializer_class = OrderSerializerList
        queryset = Order.objects.all()
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data)
