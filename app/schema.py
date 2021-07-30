from graphene import ObjectType, Scalar
from graphene import String


class ObjectIdScalar(Scalar):
    '''Object Id'''

    @staticmethod
    def serialize(id):
        return str(id)


class UserSchema(ObjectType):
    _id = ObjectIdScalar(name="_id")
    name = String()
