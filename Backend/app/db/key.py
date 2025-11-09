from loguru import logger
from typing import Optional, List
from pymongo.database import Database
from pymongo.collection import Collection
from app.model.key import KeyModel

def _get_collection(mongo_db: Database, name: str) -> Collection:
    if mongo_db is None:
        raise RuntimeError("Database connection not initialized — pass a valid mongo_db")
    return mongo_db.get_collection(name)

async def insert_dek(key_data: dict, mongo_db: Database = None) -> bool:
    """
    Insert/update a encrypted DEK.
    Returns boolean
    """
    collection = _get_collection(mongo_db, "keys")
    try:
        key = KeyModel(**key_data)
    except Exception as e:
        logger.error("Validation error: {}", e)
        return False

    filter = {"service_name": key.service_name, "userid": key.userid}
    update = {"$set": key.model_dump()}
    try:
        await collection.update_one(filter, update, upsert=True)
    except Exception as e:
        logger.error("Upsert error: {}", e)
        return False

    return True

async def get_dek(service_name: str, userid: str, mongo_db: Database = None) -> Optional[str]:
    """
    Retrieve encrypted DEK by service_name and userid.
    Returns str or None if not found.
    """
    collection = _get_collection(mongo_db, "keys")
    document = await collection.find_one({"service_name": service_name, "userid": userid})
    if document:
        return document.get("dek")
    return None

async def get_api_services(userid: str, mongo_db: Database) -> List[str]:
    """
    Retrieve a list of LLM providers associated with a given user ID.
    """
    collection = _get_collection(mongo_db, "keys")
    cursor = collection.find({"userid": userid}, {"service_name": 1, "_id": 0})
    services: List[str] = []
    async for doc in cursor:
        name = doc.get("service_name")
        if name:
            services.append(name)
    return services


async def delete_api_key(userid: str, service_name: str, mongo_db: Database = None) -> bool:
    """
    Delete encrypted DEK by service_name and userid.
    Returns boolean indicating success.
    """
    collection = _get_collection(mongo_db, "keys")
    result = await collection.delete_one({"service_name": service_name, "userid": userid})
    return result.deleted_count > 0