import graphene
from graphene_django.types import DjangoObjectType
from django.db import transaction
from .models import Customer, Product, Order
from graphene import Field, List, String, Float, Int, ID

# --------- GraphQL Types ---------
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer

class ProductType(DjangoObjectType):
    class Meta:
        model = Product

class OrderType(DjangoObjectType):
    class Meta:
        model = Order

# --------- Mutations ---------
class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = String(required=True)
        email = String(required=True)
        phone = String()

    customer = Field(CustomerType)
    message = String()

    def mutate(self, info, name, email, phone=None):
        if Customer.objects.filter(email=email).exists():
            raise Exception("Email already exists")
        customer = Customer(name=name, email=email, phone=phone)
        customer.save()
        return CreateCustomer(customer=customer, message="Customer created successfully")

class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        customers = List(lambda: CustomerInput)

    customers_created = List(CustomerType)
    errors = List(String)

    @transaction.atomic
    def mutate(self, info, customers):
        created = []
        errors = []
        for c in customers:
            if Customer.objects.filter(email=c.email).exists():
                errors.append(f"{c.email}: duplicate email")
                continue
            customer = Customer(name=c.name, email=c.email, phone=getattr(c, 'phone', None))
            customer.save()
            created.append(customer)
        return BulkCreateCustomers(customers_created=created, errors=errors)

class CustomerInput(graphene.InputObjectType):
    name = String(required=True)
    email = String(required=True)
    phone = String()

class CreateProduct(graphene.Mutation):
    class Arguments:
        name = String(required=True)
        price = Float(required=True)
        stock = Int(default_value=0)

    product = Field(ProductType)

    def mutate(self, info, name, price, stock=0):
        if price <= 0:
            raise Exception("Price must be positive")
        if stock < 0:
            raise Exception("Stock cannot be negative")
        product = Product(name=name, price=price, stock=stock)
        product.save()
        return CreateProduct(product=product)

class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_id = ID(required=True)
        product_ids = List(ID, required=True)

    order = Field(OrderType)

    def mutate(self, info, customer_id, product_ids):
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            raise Exception("Invalid customer ID")

        products = Product.objects.filter(id__in=product_ids)
        if not products:
            raise Exception("No valid products selected")

        order = Order(customer=customer)
        order.save()
        order.products.set(products)
        order.total_amount = sum([p.price for p in products])
        order.save()
        return CreateOrder(order=order)

# --------- Root Mutation ---------
class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()

# --------- Root Query (Empty for now) ---------
class CRMQuery(graphene.ObjectType):
    customers = List(CustomerType)
    hello = graphene.String(default_value="Hello, GraphQL!")

    def resolve_customers(self, info):
        return Customer.objects.all()


'''
if we run the server 8000 and go to localhost:8000/graphql
we can run the following queries and mutations:
mutation {
  bulkCreateCustomers(customers:[
    {name:"Bob", email:"bob@example.com"},
    {name:"Carol", email:"carol@example.com"}
  ]) {
    customersCreated { id name email }
    errors
  }
}

then the response will be like:
{
  "data": {
    "bulkCreateCustomers": {
      "customersCreated": [
        {
          "id": "1",
          "name": "Bob",
          "email": "bob@example.com"
        },
        {
          "id": "2",
          "name": "Carol",
          "email": "carol@example.com"
        }
      ],
      "errors": []
    }
  }
} 
'''