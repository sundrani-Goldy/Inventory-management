
import requests
from django.conf import settings
from django_tenants.utils import schema_context
from requests.exceptions import RequestException
from rest_auth.registration.views import RegisterView
from main_app.serializers.customregister import CustomRegisterSerializer
from rest_framework import status
from rest_framework.response import Response
from main_app.models.user import NewUser
from django.contrib.auth.models import Group


class CustomRegister(RegisterView):
    serializer_class = CustomRegisterSerializer
    queryset = NewUser.objects.all()


    def create(self, request, *args, **kwargs):
        serializer = CustomRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(self.request)               

        return Response("user created",
                        status=status.HTTP_201_CREATED)