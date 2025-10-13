from app.rag.embedding.pipeline import embedding_user_input
from loguru import logger
from qdrant_client.models import ScoredPoint
from app.rag.retriever.schema import Document

class EmbeddingRetriever:
    def __init__(self, model, qdrant, collection_name: str):
        self.model = model
        self.qdrant = qdrant
        self.collection_name = collection_name

    async def retrieve(self, query: str, top_k: int = 5):
        query_embedding = await embedding_user_input(self.model, query)
        categories = ["code", "documentation", "others"]
        results_by_category = {}

        for category in categories:
            # Filter by source field in Qdrant
            search_filter = {
                "must": [
                    {"key": "source", "match": {"value": category}}
                ]
            }
            results: list[ScoredPoint] = await self.qdrant.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k,
                query_filter=search_filter
            )

            documents = []
            for result in results:
                payload = dict(result.payload or {})
                chunk_text = payload.pop("chunk", "")
                payload["_score"] = getattr(result, "score", None)
                payload["_id"] = getattr(result, "id", None)
                documents.append(Document(text=chunk_text, metadata=payload))
                logger.info(f"Retrieved {category} document from Qdrant with chunk: {chunk_text[:30]}...")
            results_by_category[category] = documents

        return results_by_category