from graphene import ObjectType, Scalar
from graphene import String, Boolean


class ObjectIdScalar(Scalar):
    '''Object Id'''

    @staticmethod
    def serialize(id):
        return str(id)


class UserSchema(ObjectType):
    _id = ObjectIdScalar(name="_id")
    name = String()


class ImageSchema(ObjectType):
    _id = ObjectIdScalar(name="_id")
    url = String()
    memo = String()
    user_id = String()
    is_guide = Boolean()
