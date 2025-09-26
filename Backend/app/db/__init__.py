from dotenv import load_dotenv, find_dotenv
import os
from pymongo import MongoClient



load_dotenv(find_dotenv()) 

conn = os.getenv("MONGO_URI")
client = MongoClient(conn)

db = client["chunkDB"]
chunks_collection = db["chunks"]


