import asyncio
import uuid
from model_config import get_embedding_model
from qdrant_config import (
    get_qdrant_client,
    init_qdrant_collection,
    setup_metadata_indexes,
    COLLECTION_NAME,
)
from qdrant_client.http.models import PointStruct
from db import get_chunks, update_embedding_status

async def embedding_pipeline(batch_size: int = 50):
    model = get_embedding_model()
    qdrant = get_qdrant_client()
    init_qdrant_collection(qdrant, model.get_sentence_embedding_dimension())
    setup_metadata_indexes(qdrant)

    chunks = await get_chunks({"isEmbedded": False}, limit=batch_size)
    if not chunks:
        print("No new chunks to embed.")
        return

    texts, ids, valid_chunks = [], [], []
    for chunk in chunks:
        if "chunk" not in chunk or "chunkId" not in chunk:
            continue
        texts.append(chunk["chunk"])
        ids.append(str(uuid.uuid5(uuid.NAMESPACE_OID, chunk["chunkId"])))
        valid_chunks.append(chunk)

    embeddings = await asyncio.to_thread(model.encode, texts)
    points = [
        PointStruct(
            id=ids[i],
            vector=embeddings[i].tolist(),
            payload={k: valid_chunks[i].get(k) for k in [
                "project", "repo", "file", "section", "version", "source"
            ]} | {"original_chunkId": valid_chunks[i].get("chunkId")}
        )
        for i in range(len(valid_chunks))
    ]

    qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
    for chunk in valid_chunks:
        await update_embedding_status(chunk["chunkId"], True)

    print(f"Inserted {len(points)} embeddings and updated MongoDB.")


if __name__ == "__main__":
    asyncio.run(embedding_pipeline())
