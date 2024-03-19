from rest_framework import serializers
from store_app.models import Order,OrderDetail
from store_app.serializers.customer import CustomerSerializer

class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = '__all__'

    
class OrderSerializer(serializers.ModelSerializer):
    fk_order_detail = OrderDetailSerializer(many=True)
    fk_customer = CustomerSerializer()
    class Meta:
        model = Order
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        order_details = validated_data.pop('fk_order_detail')
        order = Order.objects.create(**validated_data)
        for order_detail in order_details:
            OrderDetail.objects.create(fk_order=order, **order_detail)
        return order