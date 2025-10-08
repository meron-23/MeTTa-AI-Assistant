import os
from dotenv import load_dotenv, find_dotenv
from qdrant_client import AsyncQdrantClient
from qdrant_client.http.models import VectorParams, Distance, PayloadSchemaType

load_dotenv(find_dotenv())
QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
COLLECTION_NAME = os.getenv("COLLECTION_NAME")


# --- Dependency injection functions (async) ---

async def get_qdrant_client(client_class=AsyncQdrantClient, host=QDRANT_HOST, port=QDRANT_PORT):
    """Injectable async Qdrant client."""
    return client_class(host=host, port=port)


async def init_qdrant_collection(qdrant_client, collection_name=COLLECTION_NAME, model_dim=None):
    """Async collection creation with dependency injection."""
    if not model_dim:
        raise ValueError("Model dimension must be provided.")

    exists = await qdrant_client.collection_exists(collection_name)
    if not exists:
        await qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=model_dim, distance=Distance.COSINE)
        )
        print(f"Collection '{collection_name}' created!")
    else:
        print(f"Collection '{collection_name}' already exists.")


async def setup_metadata_indexes(qdrant_client, collection_name=COLLECTION_NAME):
    """Async metadata indexing with dependency injection."""
    metadata_fields = {
        "chunkId": PayloadSchemaType.KEYWORD,
        "project": PayloadSchemaType.KEYWORD,
        "repo": PayloadSchemaType.KEYWORD,
        "file": PayloadSchemaType.KEYWORD,
        "section": PayloadSchemaType.KEYWORD,
        "version": PayloadSchemaType.KEYWORD,
        "source": PayloadSchemaType.KEYWORD,
    }

    for field, schema in metadata_fields.items():
        try:
            await qdrant_client.create_payload_index(
                collection_name=collection_name,
                field_name=field,
                field_schema=schema,
            )
            print(f"Created metadata index for '{field}'")
        except Exception as e:
            if "already exists" in str(e):
                print(f"Index for '{field}' already exists")
            else:
                print(f"Failed to create index for '{field}': {e}")
