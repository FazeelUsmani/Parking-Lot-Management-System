from pymongo import MongoClient
from .config import settings
from fastapi import Depends

client = MongoClient(settings.database_url)
db = client[settings.database_name]

def get_slot_collection():
    return db.slots
