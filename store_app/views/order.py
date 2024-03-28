# Create your views here.
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from store_app.models.order import *
from store_app.serializers.order import *


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
