"""
settings.py
Settings for whole application.

***Warning:***
Edit this file carefully.
"""

# Import dependencies
from datetime import timedelta
from json import loads
from pydantic import BaseModel as model
from pymongo.mongo_client import MongoClient


# Load tags
def load_tags():
    with open("config/tags.json", "r") as tags_file:
        tags = tags_file.read()
        tags_file.close()
        return loads(tags)


# Middleware configuration
class MiddlewareConfig(model):
    origins: list = ["*"]
    allow_headers: list = ["*"]
    allow_methods: list = ["GET", "POST", "PUT", "PATCH", "DELETE"]

# Database configuration
class DatabseConfig:

    # Config database
    def config_db():
        connection_url = "mongodb://localhost:27017"
        db_name = "Hustlers-Tycoon"
        client = MongoClient(connection_url)
        db = client[db_name]
        return db

    # Configure db
    db = config_db()

    # Collections
    users_collections = db["Users"]


# JWT Settings
class JWTSettings(model):
    authjwt_secret_key: str = "76b58bbfb1a8b2420d8ebe52fcbc75c6dc8a360745ebbb1cf0b9eaa39e33a668"
    authjwt_decode_algorithms: set = {"HS256","HS512"}
    access_token_exp_time: timedelta = timedelta(minutes=60*3)
    refresh_token_exp_time: timedelta = timedelta(minutes=60*4)
