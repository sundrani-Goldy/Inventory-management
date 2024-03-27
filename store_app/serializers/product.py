from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from store_app.models import Product, ProductImage, Category, Tag, Tax, Discount


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'fk_product']

    def create(self, validated_data):
        return super().create(validated_data)


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField(), write_only=True)
    fk_category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True, required=False)
    fk_tag = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False)
    fk_tax = serializers.PrimaryKeyRelatedField(queryset=Tax.objects.all(), many=True, required=False)
    discount = serializers.PrimaryKeyRelatedField(queryset=Discount.objects.all(), many=True, required=False)
    product_images = ProductImageSerializer(many=True, read_only=True, source='productimage_set')

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['fk_category'] = [{'id': category.id, 'name': category.name} for category in
                                         instance.fk_category.all()]
        representation['fk_tag'] = [{'id': tag.id, 'name': tag.name} for tag in instance.fk_tag.all()]
        representation['fk_tax'] = [{'id': tax.id, 'name': tax.name} for tax in instance.fk_tax.all()]
        representation['discount'] = [{'id': discount.id, 'name': discount.name} for discount in
                                      instance.discount.all()]

        return representation

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        if len(images_data) > 5:
            raise ValidationError("You can upload a maximum of 5 images.")
        fk_category_data = validated_data.pop('fk_category', [])
        fk_tag_data = validated_data.pop('fk_tag', [])
        fk_tax_data = validated_data.pop('fk_tax', [])
        discount_data = validated_data.pop('discount', [])

        product = Product.objects.create(**validated_data)

        product.fk_category.set(fk_category_data)
        product.fk_tag.set(fk_tag_data)
        product.fk_tax.set(fk_tax_data)
        product.discount.set(discount_data)

        for image_data in images_data:
            ProductImage.objects.create(fk_product=product, image=image_data)

        return product

    def partial_update(self, instance, validated_data):
        fk_category_data = validated_data.pop('fk_category', [])
        fk_tag_data = validated_data.pop('fk_tag', [])
        fk_tax_data = validated_data.pop('fk_tax', [])
        discount_data = validated_data.pop('discount', [])

        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.base_price = validated_data.get('base_price', instance.base_price)
        instance.sell_price = validated_data.get('sell_price', instance.sell_price)
        instance.mrp = validated_data.get('mrp', instance.mrp)
        instance.save()

        instance.fk_category.set(fk_category_data)
        instance.fk_tag.set(fk_tag_data)
        instance.fk_tax.set(fk_tax_data)
        instance.discount.set(discount_data)

        updated_product = Product.objects.get(pk=instance.pk)
        return updated_product
