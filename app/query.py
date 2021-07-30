
import graphene
from bson import ObjectId
from database import db
from schema import UserSchema


class Query(graphene.ObjectType):
    user_list = graphene.List(UserSchema)
    user = graphene.Field(UserSchema, id=graphene.String())

    def resolve_user_list(self, info):
        user_list = db.user.find()
        return list(user_list)

    def resolve_user(self, info, id):
        user = db.user.find_one({"_id": ObjectId(id)})
        return user
