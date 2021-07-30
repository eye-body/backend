import graphene
from database import db
from schema import UserSchema


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


class Mutations(graphene.ObjectType):
    create_user = CreateUser.Field()
