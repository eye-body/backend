import auth
import graphene
from database import db
from schema import UserSchema, ImageSchema


class UserInput(graphene.InputObjectType):
    email = graphene.String(required=True)
    name = graphene.String(required=True)
    password = graphene.String(required=True)


class ImageInput(graphene.InputObjectType):
    image = graphene.String(required=True)
    memo = graphene.String()
    is_guide = graphene.Boolean(default=False)


class CreateUser(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)

    user = graphene.Field(UserSchema)

    def mutate(root, info, input: UserInput):
        new_user = db.user.insert_one(input)
        created_user = db.user.find_one({"_id": new_user.inserted_id})
        return CreateUser(user=created_user)


def upload_image(image):
    import boto3
    import base64
    from datetime import datetime
    s3 = boto3.resource("s3")
    bucket = s3.Bucket("eye-body")
    path = f"image/{datetime.now().isoformat()}.jpg"
    bucket.put_object(
        Key=path,
        Body=base64.b64decode(image),
        ContentType="image/jpg"
    )
    bucket_url = "https://eye-body.s3.ap-northeast-2.amazonaws.com"
    return f"{bucket_url}/{path}"


class CreateImage(graphene.Mutation):
    class Arguments:
        input = ImageInput(required=True)

    image = graphene.Field(ImageSchema)

    def mutate(root, info, input: ImageInput):
        jwt = info.context.get("request").headers.get("Authorization")
        id = auth.jwt_required(jwt)["_id"]
        url = upload_image(input.image)

        data = {
            "url": url,
            "memo": input.memo,
            "user_id": id,
            "is_guide": True if input.is_guide else False
        }
        new_image = db.image.insert_one(data)
        created_image = db.image.find_one({"_id": new_image.inserted_id})
        return CreateImage(image=created_image)


class UserTokenInput(graphene.InputObjectType):
    email = graphene.String(required=True)
    password = graphene.String(required=True)


class GetUserToken(graphene.Mutation):
    class Arguments:
        input = UserTokenInput(required=True)

    token = graphene.String()
    user = graphene.Field(UserSchema)

    def mutate(root, info, input: UserInput):
        user = db.user.find_one(input)
        token = auth.token_response({"_id": str(user["_id"])})
        return GetUserToken(user=user, token=token)


class Mutations(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_image = CreateImage.Field()
    get_user_token = GetUserToken.Field()
