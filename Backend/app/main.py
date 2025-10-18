from fastapi import FastAPI, Request, Response
import time
from loguru import logger
from contextlib import asynccontextmanager
from typing import AsyncIterator, Dict
from app.routers import chunks
from pymongo import AsyncMongoClient
import os
from pymongo.errors import PyMongoError
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info("Application has started")
    mongo_uri = os.getenv("MONGO_URI")
    mongo_db_name = os.getenv("MONGO_DB")
    if not mongo_uri:
        logger.error("MONGO_URI is not set. Please set the MONGO_URI environment variable.")
        raise RuntimeError("MONGO_URI environment variable is required")
    
    if not mongo_db_name:
        logger.error("MONGO_DB is not set. Please set the MONGO_DB environment variable.")
        raise RuntimeError("MONGO_DB environment variable is required")

    app.state.mongo_client = AsyncMongoClient(mongo_uri)
    app.state.mongo_db = app.state.mongo_client[mongo_db_name]

    # Validate connection by issuing a ping. If ping fails, close the client and stop startup.
    try:
        await app.state.mongo_db.command({"ping": 1})
        logger.info("Successfully connected to MongoDB")
    except PyMongoError as e:
        logger.exception("Failed to connect to MongoDB: {}", e)
        try:
            await app.state.mongo_client.close()
        except Exception:
            logger.exception("Error while closing MongoDB client after failed connect")
        raise RuntimeError("Unable to connect to MongoDB") from e

    try:
        yield
    finally:
        try:
            await app.state.mongo_client.close()
            logger.info("MongoDB client closed")
        except Exception:
            logger.exception("Error closing MongoDB client during shutdown")

    logger.info("Application shutting down .....")

app = FastAPI(lifespan=lifespan)
app.include_router(chunks.router)


@app.middleware("http") 
async def log_requests(request: Request, call_next) -> Response:
    start_time = time.time()
    response = await call_next(request)
    duration_ms = int((time.time() - start_time) * 1000)
    logger.info(
        f"{request.method} {request.url.path} -> {response.status_code} ({duration_ms} ms)"
    )
    return response

@app.get("/health")
def health_check() -> Dict[str, str]:
    return {"status": "ok"}
