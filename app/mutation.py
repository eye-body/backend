import graphene
from database import db
from schema import UserSchema


class UserInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    password = graphene.String(required=True)


class CreateUser(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)

    user = graphene.Field(UserSchema)

    def mutate(root, info, input: UserInput):
        new_user = db.user.insert_one(input)
        created_user = db.user.find_one({"_id": new_user.inserted_id})
        return CreateUser(user=created_user)


class Mutations(graphene.ObjectType):
    create_user = CreateUser.Field()
