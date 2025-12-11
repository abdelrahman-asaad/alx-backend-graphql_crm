import graphene

class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello, GraphQL!") #name of the query 'hello'

schema = graphene.Schema(query=Query)
