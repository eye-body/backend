import graphene


class ObjectIdScalar(graphene.Scalar):
    '''Object Id'''

    @staticmethod
    def serialize(id):
        return str(id)


class UserSchema(graphene.ObjectType):
    _id = ObjectIdScalar(name="_id")
    email = graphene.String()
    name = graphene.String()


class ImageSchema(graphene.ObjectType):
    _id = ObjectIdScalar(name="_id")
    url = graphene.String()
    memo = graphene.String()
    user_id = graphene.String()
    is_guide = graphene.Boolean()
