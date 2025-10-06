from pydantic import BaseModel
from typing import Literal, List, Optional
from pymongo.errors import BulkWriteError


# Set up MongoDB schema/collections for chunks and metadata.
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

# Function to insert a single chunk into the MongoDB collection with validation.
async def insert_chunk(chunk_data: dict, mongo_db: Optional[any] = None) -> str | None:
    """
    Insert a single chunk.
    Returns inserted ID.
    """
    collection = mongo_db.get_collection("chunks") if mongo_db is not None else None
    if collection is None:
        raise RuntimeError("mongo_db must be provided")
    chunk = ChunkSchema(**chunk_data)
    if await collection.find_one({"chunkId": chunk.chunkId}):
        print(f"Chunk with chunkId '{chunk.chunkId}' already exists.")
        return None
    result = await collection.insert_one(chunk.model_dump())
    return chunk.chunkId

# Function to insert many chunks into the MongoDB collection with validation.
async def insert_chunks(
    chunks_data: List[dict], mongo_db: Optional[any] = None
) -> List[str]:
    """
    Insert multiple chunks with duplicate checking.
    Returns a list of inserted chunkIds.
    """
    collection = mongo_db.get_collection("chunks") if mongo_db is not None else None
    if collection is None:
        raise RuntimeError("mongo_db must be provided")
    valid_chunks = []

    # Validate and check duplicates
    for chunk_data in chunks_data:
        try:
            chunk = ChunkSchema(**chunk_data)
            if not await collection.find_one({"chunkId": chunk.chunkId}):
                valid_chunks.append(chunk.model_dump())
            else:
                print(f"Skipping duplicate chunkId: {chunk.chunkId}")
        except Exception as e:
            print("Validation error:", e)

    if not valid_chunks:
        return []

    # Insert many
    try:
        result = await collection.insert_many(valid_chunks, ordered=False)
        inserted_ids = result.inserted_ids
    except BulkWriteError as e:
        print("Some duplicates were skipped.", e.details)
        inserted_ids = e.details.get("writeErrors", [])
        # Extract inserted ids if available
        inserted_ids = [item["op"]["chunkId"] for item in inserted_ids if "op" in item and "chunkId" in item["op"]]

    # Return list of inserted chunkIds
    return [chunk["chunkId"] for chunk in valid_chunks]


# Function to retrieve  chunks by ChunkId from the MongoDB collection.
async def get_chunk_by_id(chunk_id: str, mongo_db: Optional[any] = None) -> dict | None:
    """
    Retrieve a chunk by its ID.
    """
    collection = mongo_db.get_collection("chunks") if mongo_db is not None else None
    if collection is None:
        raise RuntimeError("mongo_db must be provided")
    return await collection.find_one({"chunkId": chunk_id}, {"_id": 0})


# Function to retrieve all chunks from the MongoDB collection.
async def get_chunks(
    filter_query: dict = None, limit: int = 10, mongo_db: Optional[any] = None
) -> List[dict]:
    """
    Retrieve multiple chunks matching the filter.
    Returns a list of dictionaries.
    """
    collection = mongo_db.get_collection("chunks") if mongo_db is not None else None
    if collection is None:
        raise RuntimeError("mongo_db must be provided")
    filter_query = filter_query or {}
    cursor = collection.find(filter_query, {"_id": 0}).limit(limit)
    return [doc async for doc in cursor]

# Function to update embedding status of a chunk by chunkId.
async def update_embedding_status(
    chunk_id: str, status: bool, mongo_db: Optional[any] = None
) -> int:
    """
    Update the embedding status of a chunk.
    """
    collection = mongo_db.get_collection("chunks") if mongo_db is not None else None
    if collection is None:
        raise RuntimeError("mongo_db must be provided")
    result = await collection.update_one(
        {"chunkId": chunk_id}, {"$set": {"isEmbedded": status}}
    )
    return result.modified_count


# Function to update any fields of a single chunk by chunkID.
async def update_chunk(
    chunk_id: str, updates: dict, mongo_db: Optional[any] = None
) -> int:
    """
    Update any fields of a single chunk by chunkId.
    Returns the number of documents modified (0 or 1).
    """
    collection = mongo_db.get_collection("chunks") if mongo_db is not None else None
    if collection is None:
        raise RuntimeError("mongo_db must be provided")
    result = await collection.update_one({"chunkId": chunk_id}, {"$set": updates})
    return result.modified_count

# Function to update multiple chunks matching a filter query.
async def update_chunks(
    filter_query: dict, updates: dict, mongo_db: Optional[any] = None
) -> int:
    """
    Update any fields for multiple chunks matching the filter.
    Returns the number of documents modified.
    """
    collection = mongo_db.get_collection("chunks") if mongo_db is not None else None
    if collection is None:
        raise RuntimeError("mongo_db must be provided")
    result = await collection.update_many(filter_query, {"$set": updates})
    return result.modified_count

# Function to delete a chunk by chunkId.
async def delete_chunk(chunk_id: str, mongo_db: Optional[any] = None) -> int:
    """
    Delete a chunk by its ID.
    """
    collection = mongo_db.get_collection("chunks") if mongo_db is not None else None
    if collection is None:
        raise RuntimeError("mongo_db must be provided")
    result = await collection.delete_one({"chunkId": chunk_id})
    return result.deleted_count
