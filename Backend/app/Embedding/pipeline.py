import asyncio
import uuid
from model_config import get_embedding_model
from qdrant_config import (
    get_qdrant_client,
    init_qdrant_collection,
    setup_metadata_indexes,
    COLLECTION_NAME,
)
from qdrant_client.models import PointStruct  # use models instead of http.models
from db import get_chunks, update_embedding_status
from qdrant_client import AsyncQdrantClient

async def embedding_pipeline(batch_size: int = 50):
    # Load model
    model = get_embedding_model()

    # Async Qdrant client
    qdrant: AsyncQdrantClient = await get_qdrant_client()

    # Async collection initialization
    await init_qdrant_collection(qdrant, model_dim=model.get_sentence_embedding_dimension())
    await setup_metadata_indexes(qdrant)

    # Fetch chunks from MongoDB asynchronously
    chunks = await get_chunks({"isEmbedded": False}, limit=batch_size)
    if not chunks:
        print("No new chunks to embed.")
        return

    # Prepare texts and ids
    texts, ids, valid_chunks = [], [], []
    for chunk in chunks:
        if "chunk" not in chunk or "chunkId" not in chunk:
            continue
        texts.append(chunk["chunk"])
        ids.append(str(uuid.uuid5(uuid.NAMESPACE_OID, chunk["chunkId"])))
        valid_chunks.append(chunk)

    # Generate embeddings asynchronously
    embeddings = await asyncio.to_thread(model.encode, texts)

    # Prepare points
    points = [
        PointStruct(
            id=ids[i],
            vector=embeddings[i].tolist(),
            payload={
                **{k: valid_chunks[i].get(k) for k in ["project", "repo", "file", "section", "version", "source"]},
                "original_chunkId": valid_chunks[i].get("chunkId")
            }
        )
        for i in range(len(valid_chunks))
    ]

    # Async upsert into Qdrant
    await qdrant.upsert(collection_name=COLLECTION_NAME, points=points)

    # Update MongoDB embedding status asynchronously
    for chunk in valid_chunks:
        await update_embedding_status(chunk["chunkId"], True)

    print(f"Inserted {len(points)} embeddings and updated MongoDB.")


if __name__ == "__main__":
    asyncio.run(embedding_pipeline())
