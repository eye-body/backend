
from pymongo import MongoClient
from decouple import config

client = MongoClient(config("MONGODB_URI"))
db = client.eye_body
