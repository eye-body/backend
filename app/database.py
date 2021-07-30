
import os
from pymongo import MongoClient

client = MongoClient(
    os.environ["MONGODB_URI"]
)
db = client.eye_body
