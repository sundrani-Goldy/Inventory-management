from rest_framework import serializers
from tenant_app.models import Domain
from tenant_app.models import Store


class DomainSerializer(serializers.ModelSerializer):
    schema = serializers.SerializerMethodField()

    def get_schema(self, obj):
        return obj.tenant.schema_name  # Accessing the schema name from the related Tenant instance

    class Meta:
        model = Domain
        fields = ['domain', 'schema']