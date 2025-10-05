from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance, PayloadSchemaType

#set up Qdrant client and collection
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
COLLECTION_NAME = "code_chunks"

def get_qdrant_client():
    return QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

def init_qdrant_collection(qdrant, model_dim: int):
    if not qdrant.collection_exists(COLLECTION_NAME):
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=model_dim, distance=Distance.COSINE)
        )
        print(f"Collection '{COLLECTION_NAME}' created!")
    else:
        print(f"Collection '{COLLECTION_NAME}' already exists.")

#enable metadata indexing
def setup_metadata_indexes(qdrant):
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
            qdrant.create_payload_index(
                collection_name=COLLECTION_NAME,
                field_name=field,
                field_schema=schema,
            )
            print(f" Created metadata index for '{field}'")
        except Exception as e:
            if "already exists" in str(e):
                print(f"Index for '{field}' already exists")
            else:
                print(f"Failed to create index for '{field}': {e}")
