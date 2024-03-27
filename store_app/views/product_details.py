import os

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from store_app.models import Variant, VariantImage
from store_app.serializers.product_details import VariantSerializer, VariantImageSerializer


class VariantViewSet(viewsets.ModelViewSet):
    queryset = Variant.objects.all()
    serializer_class = VariantSerializer

    def partial_update(self, request, pk=None):
        instance = self.get_object()
        serializer = VariantSerializer(instance, data=request.data , partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass


class VariantImageViewSet(viewsets.ModelViewSet):
    queryset = VariantImage.objects.all()
    serializer_class = VariantImageSerializer

    def create(self, request, *args, **kwargs):
        serializer = VariantImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        fk_variant = serializer.validated_data.get('fk_variant')

        if fk_variant.variantimage_set.count() >= 5:
            return Response({"error":"You can upload maximun five images"}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        file_path = instance.image.path

        if os.path.exists(file_path):
            os.remove(file_path)

        instance.delete()

        return Response({"message": "Image deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        pass

    def update(self, request, *args, **kwargs):
        pass

    def partial_update(self, request, *args, **kwargs):
        pass
