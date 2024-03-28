from rest_framework import serializers

from store_app.models import Customer
from store_app.models import Order, OrderDetail, Warehouse, Discount, Tax, Tag
from store_app.serializers.customer import CustomerSerializer
from store_app.serializers.tag import TagSerializer
from store_app.serializers.tax_and_discount import DiscountSerializer, TaxSerializer
from store_app.serializers.warehouse import WarehouseSerializer


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    fk_order_detail = OrderDetailSerializer(many=True)
    fk_customer = CustomerSerializer()
    fk_discount = serializers.PrimaryKeyRelatedField(queryset=Discount.objects.all())
    fk_warehouse = serializers.PrimaryKeyRelatedField(queryset=Warehouse.objects.all())
    fk_other_tax = serializers.PrimaryKeyRelatedField(queryset=Tax.objects.all())
    fk_tag = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)  
    sub_total = serializers.IntegerField()
    final_price = serializers.IntegerField()

    class Meta:
        model = Order
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['fk_discount'] = DiscountSerializer(instance.fk_discount).data
        rep['fk_warehouse'] = WarehouseSerializer(instance.fk_warehouse).data
        rep['fk_other_tax'] = TaxSerializer(instance.fk_other_tax).data
        rep['fk_tag'] = TagSerializer(instance.fk_tag.all(), many=True).data
        return rep


    def create(self, validated_data):
        order_detail_data = validated_data.pop('fk_order_detail')
        fk_customer_data = validated_data.pop('fk_customer')
        fk_tag_ids = validated_data.pop('fk_tag', [])
        fk_discount_instance = validated_data.pop('fk_discount')
        fk_warehouse_instance = validated_data.pop('fk_warehouse')
        fk_other_tax_instance = validated_data.pop('fk_other_tax')

        fk_customer_instance, _ = Customer.objects.get_or_create(mobile_number=fk_customer_data['mobile_number'], defaults=fk_customer_data)

        order_instance = Order.objects.create(fk_customer=fk_customer_instance, fk_discount=fk_discount_instance, fk_warehouse=fk_warehouse_instance, fk_other_tax=fk_other_tax_instance, **validated_data)

        order_instance.fk_tag.set(fk_tag_ids)  
        orders = []
        for order_detail in order_detail_data:
            order = OrderDetail.objects.create(order=order_instance, **order_detail)
            orders.append(order)
        order_instance.fk_order_detail.set(orders)

        return order_instance
    
    def update(self, instance, validated_data):
        order_detail_data = validated_data.pop('fk_order_detail')
        fk_customer_data = validated_data.pop('fk_customer')
        fk_tag_ids = validated_data.pop('fk_tag', [])
        fk_discount_instance = validated_data.pop('fk_discount')
        fk_warehouse_instance = validated_data.pop('fk_warehouse')
        fk_other_tax_instance = validated_data.pop('fk_other_tax')

        fk_customer_instance, _ = Customer.objects.update_or_create(mobile_number=fk_customer_data['mobile_number'], defaults=fk_customer_data)

        instance.fk_customer = fk_customer_instance
        instance.fk_discount = fk_discount_instance
        instance.fk_warehouse = fk_warehouse_instance
        instance.fk_other_tax = fk_other_tax_instance
        instance.save()

        instance.fk_tag.set(fk_tag_ids)

        instance.fk_order_detail.all().delete()
        orders = []
        for order_detail in order_detail_data:
            order = OrderDetail.objects.create(order=instance, **order_detail)
            orders.append(order)
        instance.fk_order_detail.set(orders)

        return instance




class OrderSerializerList(serializers.ModelSerializer):
    product_name_and_discount = serializers.SerializerMethodField()
    customer_name = serializers.CharField(source='fk_customer.name')
    customer_mobile_number = serializers.CharField(source='fk_customer.mobile_number')
    warehouse_name = serializers.CharField(source='fk_warehouse.name')
    tag = serializers.SerializerMethodField()
    final_price = serializers.IntegerField()
    discount = serializers.DecimalField(source='fk_discount.amount', max_digits=10, decimal_places=2)
    discount_type = serializers.CharField(source='fk_discount.discount_option')

    class Meta:
        model = Order
        fields = ['id', 'product_name_and_discount', 'customer_name', 'customer_mobile_number', 'warehouse_name', 'tag', 'final_price','discount', 'discount_type']

    def get_product_name_and_discount(self, obj):
        products = [order_detail.fk_product.name for order_detail in obj.fk_order_detail.all()]
        discounts = [order_detail.fk_discount.amount for order_detail in obj.fk_order_detail.all()]
        discounts_type = [order_detail.fk_discount.discount_option for order_detail in obj.fk_order_detail.all()]
        product_price = [order_detail.price for order_detail in obj.fk_order_detail.all()]

        return [{'product': product, 'discount': discount, 'discount_type': discount_type, 'price': price} for product, discount, discount_type, price in zip(products, discounts, discounts_type, product_price)]

        

    
    def get_tag(self, obj):
        return [tag.name for tag in obj.fk_tag.all()]
