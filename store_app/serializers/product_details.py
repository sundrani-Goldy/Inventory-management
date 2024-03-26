from rest_framework import serializers
from store_app.models.product_detail import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = '__all__'


class ExtraDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraDetails
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields= '__all__'