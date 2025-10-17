from fastapi import Request, Depends
from pymongo.database import Database 
from sentence_transformers import SentenceTransformer
from qdrant_client import AsyncQdrantClient
from decouple import config 
from app.repositories.chunk_repository import ChunkRepository
from app.services.llm_service import BaseLLMProvider, GeminiLLMProvider
from app.services.chunk_annotation_service import ChunkAnnotationService


def get_mongo_client(request: Request):
    return request.app.state.mongo_client

def get_mongo_db(request: Request) -> Database:
    return request.app.state.mongo_db

def get_embedding_model_dep(request: Request) -> SentenceTransformer:
    return request.app.state.embedding_model

def get_qdrant_client_dep(request: Request) -> AsyncQdrantClient:
    """Return Qdrant client stored in app.state"""
    return request.app.state.qdrant_client


def get_chunk_repository(db: Database = Depends(get_mongo_db)) -> ChunkRepository:
    """Returns the ChunkRepository instance, injected with the DB."""
    return ChunkRepository(db)


def get_llm_provider() -> BaseLLMProvider:
    """Returns the configured LLM Provider instance."""
    # Securely retrieve the API key using python-decouple
    gemini_api_key = config("GEMINI_API_KEY", default=None)
    
    if not gemini_api_key:
         # Raise an error or log a critical warning if the key is missing
         print("CRITICAL CONFIG ERROR: GEMINI_API_KEY is not set.")
    
    return GeminiLLMProvider(api_key=gemini_api_key)


def get_annotation_service(
    repository: ChunkRepository = Depends(get_chunk_repository),
    llm_provider: BaseLLMProvider = Depends(get_llm_provider)
) -> ChunkAnnotationService:
    """Returns the ChunkAnnotationService instance, orchestrating the pipeline."""
    return ChunkAnnotationService(
        repository=repository, 
        llm_provider=llm_provider
    )