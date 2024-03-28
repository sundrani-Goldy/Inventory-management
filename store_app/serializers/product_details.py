from rest_framework import serializers
from store_app.models.product_detail import *
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ListSerializer

from store_app.models import Category, Variant, ExtraDetails, VariantImage, Tag

from store_app.models.product_detail import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class VariantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantImage
        fields = ['id', 'image', 'fk_variant']  # Include 'fk_variant' to check the value being passed

    def create(self, validated_data):
        return super().create(validated_data)
class VariantSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField(),write_only=True)
    fk_tag = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),many=True , required=False)
    variant_image = VariantImageSerializer(many=True,read_only=True ,source='variantimage_set')


    def to_representation(self, instance):

        representation = super().to_representation(instance)
        representation['fk_tag'] = [{'id': tag.id, 'name': tag.name} for tag in instance.fk_tag.all()]
        return representation


    class Meta:
        model = Variant
        fields = '__all__'

    def create(self, validated_data):
        images_data = validated_data.pop('images',[])
        if len(images_data) > 5 :
            raise ValidationError('You can upload maximum 5 images')

        fk_tag_data = validated_data.pop('fk_tag', [])

        variant = Variant.objects.create(**validated_data)

        variant.fk_tag.set(fk_tag_data)

        for image in images_data:
            VariantImage.objects.create(fk_variant=variant, image=image)

        return variant

    def partial_update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.fk_tag.set(validated_data.get('fk_tag', instance.fk_tag.all()))

        instance.save()
        updated_data = Variant.objects.get(pk=instance.pk)
        return updated_data

class ExtraDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraDetails
        fields = '__all__'
