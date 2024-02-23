import graphene
from graphene_django.types import DjangoObjectType
from .models import Product, ProductImage

class ProductType(DjangoObjectType):
    class Meta:
        model = Product

class ProductImageType(DjangoObjectType):
    class Meta:
        model = ProductImage

class Query(graphene.ObjectType):
    all_products = graphene.List(ProductType)

    def resolve_all_products(self, info, **kwargs):
        return Product.objects.all()

class ProductInput(graphene.InputObjectType):
    name = graphene.String()
    description = graphene.String()
    base_price = graphene.String()
    sell_price = graphene.String()
    mrp = graphene.String()
    # Add other fields as needed


class CreateProduct(graphene.Mutation):
    class Arguments:
        input = ProductInput(required=True)

    product = graphene.Field(ProductType)

    def mutate(self, info, input):
        product_data = input
        product = Product.objects.create(**product_data)
        return CreateProduct(product=product)


class Mutation(graphene.ObjectType):
    create_product = CreateProduct.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
