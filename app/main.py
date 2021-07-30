import os
from typing import List, Optional
from bson import ObjectId
from fastapi import FastAPI, Body
import graphene
from graphene.types import Scalar
from starlette.graphql import GraphQLApp
from pydantic import BaseModel, Field
from pymongo import MongoClient

from schema import UserSchema

client = MongoClient(
    os.environ["MONGODB_URI"]
)
db = client.eye_body


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    name: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UserInputModel(BaseModel):
    name: str


class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="stranger"))
    user_list = graphene.List(UserSchema)
    user = graphene.Field(UserSchema, id=graphene.String())

    def resolve_hello(self, info, name):
        return "Hi " + name

    def resolve_user_list(self, info):
        user_list = db.user.find()
        return list(user_list)

    def resolve_user(self, info, id):
        user = db.user.find_one({"_id": ObjectId(id)})
        return user


class CreateUser(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    success = graphene.Boolean()
    user = graphene.Field(lambda: UserSchema)

    def mutate(root, info, name):
        new_user = db.user.insert_one({"name": name})
        created_user = db.user.find_one({"_id": new_user.inserted_id})
        success = True
        return CreateUser(success=success, user=created_user)


class MyMutations(graphene.ObjectType):
    create_user = CreateUser.Field()


app = FastAPI()
app.add_route(
    "/graphql", GraphQLApp(schema=graphene.Schema(query=Query, mutation=MyMutations)))


@app.post(
    "/users", response_description="Add new user", response_model=UserModel
)
def create_user(user: UserInputModel = Body(...)):
    new_user = db.user.insert_one(user.dict(exclude={"id"}))
    created_user = db.user.find_one({"_id": new_user.inserted_id})
    return created_user


@app.get(
    "/users",
    response_description="List all users",
    response_model=List[UserModel],
)
def get_user_list():
    user_list = db["user"].find()
    return list(user_list)
