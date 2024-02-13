from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers


class CustomRegisterSerializer(RegisterSerializer):
    is_superuser = serializers.BooleanField(required=False)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)

    def custom_signup(self, request, user):
        if self.validated_data.get('is_superuser'):
            user.is_superuser = True
            user.is_staff = True
            user.is_active = True
            user.save()
        user.first_name = self.validated_data.get("first_name")

        user.last_name = self.validated_data.get("last_name")
        user.save()
