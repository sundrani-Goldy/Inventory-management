from rest_framework import serializers

from store_app.models import Category, Variant, ExtraDetails


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
