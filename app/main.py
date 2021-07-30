from fastapi import FastAPI
import graphene
from starlette.graphql import GraphQLApp
from query import Query
from mutation import Mutations

app = FastAPI()
app.add_route(
    "/graphql", GraphQLApp(schema=graphene.Schema(query=Query, mutation=Mutations)))
