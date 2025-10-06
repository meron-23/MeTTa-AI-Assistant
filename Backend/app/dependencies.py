from fastapi import Request
from pymongo import AsyncMongoClient


def get_mongo_client(request: Request) -> AsyncMongoClient:
    return request.app.state.mongo_client


def get_mongo_db(request: Request):
    return request.app.state.mongo_db
