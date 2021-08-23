import time
from typing import Any, Dict

import jwt
from decouple import config

JWT_SECRET = config("SECRET_KEY")
JWT_ALGORITHM = config("ALGORITHM")


def token_response(seed: Dict[str, Any]):
    return jwt.encode(seed, JWT_SECRET, algorithm=JWT_ALGORITHM)


def jwt_required(token):
    return jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
