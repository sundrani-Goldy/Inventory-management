from rest_framework import serializers

from store_app.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
