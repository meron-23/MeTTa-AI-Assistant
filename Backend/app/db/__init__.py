from dotenv import load_dotenv, find_dotenv
import os
from pymongo import MongoClient
from pydantic import BaseModel, Field
from typing import Literal


load_dotenv(find_dotenv()) 

conn = os.getenv("MONGO_URI")
client = MongoClient(conn)

db = client["chunkDB"]
chunks_collection = db["chunks"]


class ChunkSchema(BaseModel):
    chunkId: str 
    source: Literal["code", "specification", "documentation"]
    chunk: str
    project: str
    repo: str
    section: str
    file: str
    version: str
    isEmbedded: bool = False
