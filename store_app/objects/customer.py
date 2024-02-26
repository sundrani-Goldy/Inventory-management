import graphene
from graphene_django.types import DjangoObjectType
from store_app.models import Customer



class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer

class CustomerInput(graphene.InputObjectType):
    name = graphene.String()
    mobile_number = graphene.String()
    email = graphene.String()
    company_name = graphene.String()
    address = graphene.String()
    city = graphene.String()
    state = graphene.String()
    country = graphene.String()
    pincode = graphene.Int()
    
class ListCustomer(graphene.ObjectType):
    all_customers = graphene.List(Customer)

    def resolve_all_customers(self, info, **kwargs):
        return Customer.objects.all()


class CreateCustomer(graphene.Mutation):
    class Arguments:
        input = CustomerInput(required=True)

    customer = graphene.Field(CustomerType)

    def mutate(self, info, input):
        customer_data = input
        customer = Customer.objects.create(**customer_data)
        return CreateCustomer(customer=customer)



    

