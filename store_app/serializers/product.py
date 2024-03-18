from rest_framework import serializers
from store_app.models import Product, ProductImage

from rest_framework.exceptions import ValidationError

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from rest_framework import serializers
from store_app.models import Product, ProductImage



class ProductSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField(), write_only=True)

    class Meta:
        model = Product
        fields = ['id', 'fk_category', 'fk_variant', 'fk_extra_detail', 'fk_tag', 'name', 'description', 'base_price', 'sell_price', 'mrp', 'fk_tax', 'discount', 'created_at', 'images']

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])  # Extracting images data from validated data

        # Handle many-to-many relationships separately
        fk_category = validated_data.pop('fk_category', [])
        fk_variant = validated_data.pop('fk_variant', [])
        fk_extra_detail = validated_data.pop('fk_extra_detail', [])
        fk_tag = validated_data.pop('fk_tag', [])
        fk_tax = validated_data.pop('fk_tax', [])
        discount = validated_data.pop('discount', [])

        product = Product.objects.create(**validated_data)

        # Assign many-to-many fields to product
        product.fk_category.set(fk_category)
        product.fk_variant.set(fk_variant)
        product.fk_extra_detail.set(fk_extra_detail)
        product.fk_tag.set(fk_tag)
        product.fk_tax.set(fk_tax)
        product.discount.set(discount)

        # Create product images and assign tags
        for image_data in images_data:
            ProductImage.objects.create(fk_product=product, image=image_data)

        return product

