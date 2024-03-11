from rest_framework import serializers
from store_app.models import Product, ProductImage

from rest_framework.exceptions import ValidationError

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class ProductSerializer(serializers.ModelSerializer):
    images = serializers.ListSerializer(child=serializers.ImageField(), required=True)

    class Meta:
        model = Product
        fields = ['id', 'fk_category', 'fk_variant', 'fk_extra_detail', 'fk_tag', 'name', 'description', 'base_price', 'sell_price', 'mrp', 'fk_tax', 'discount', 'created_at', 'images']

    def create(self, validated_data):
        print('in create')
        images_data = validated_data.pop('images')
        product = Product.objects.create(**validated_data)
        for image_data in images_data:
            ProductImage.objects.create(fk_product=product, image=image_data)
        return product

    def validate(self, attrs):
        print('inside ser')
        request = self.context.get('request')
        if not request.FILES.getlist('images'):
            raise ValidationError("Images field is required.")
        return attrs

