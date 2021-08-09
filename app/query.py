
import graphene
from bson import ObjectId
from database import db
from schema import UserSchema, ImageSchema


class Query(graphene.ObjectType):
    user_list = graphene.List(UserSchema)
    user = graphene.Field(UserSchema, id=graphene.String())
    image_list = graphene.List(ImageSchema, user_id=graphene.String())
    image = graphene.Field(ImageSchema, id=graphene.String())

    def resolve_user_list(self, info):
        user_list = db.user.find()
        return list(user_list)

    def resolve_user(self, info, id):
        user = db.user.find_one({"_id": ObjectId(id)})
        return user

    def resolve_image_list(self, info, user_id=None):
        if user_id:
            image_list = db.image.find({"user_id": user_id})
        else:
            image_list = db.image.find()
        return list(image_list)

    def resolve_image(self, info, id):
        image = db.image.find_one({"_id": ObjectId(id)})
        return image
