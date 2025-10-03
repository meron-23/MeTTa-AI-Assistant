from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional, Dict, Any
from pydantic import BaseModel
from app.db.db import update_chunk, delete_chunk, get_chunk_by_id, ChunkSchema
from bson import ObjectId

router = APIRouter(
    prefix="/api/chunks",
    tags=["chunks"],
    responses={404: {"description": "Not found"}},
)

class ChunkUpdate(BaseModel):
    source: Optional[str] = None
    chunk: Optional[str] = None
    project: Optional[str] = None
    repo: Optional[str] = None
    section: Optional[str] = None
    file: Optional[str] = None
    version: Optional[str] = None
    isEmbedded: Optional[bool] = None

@router.patch("/{chunk_id}", response_model=Dict[str, Any])
async def update_chunk_endpoint(chunk_id: str, chunk_update: ChunkUpdate):
    """
    Update a chunk by its ID.
    Only the fields provided in the request body will be updated.
    """
    update_data = {k: v for k, v in chunk_update.dict().items() if v is not None}
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No update data provided"
        )
    
    existing_chunk = await get_chunk_by_id(chunk_id)
    if not existing_chunk:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chunk with ID {chunk_id} not found"
        )
    

    updated_count = await update_chunk(chunk_id, update_data)
    if updated_count == 0:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update chunk"
        )
    
    updated_chunk = await get_chunk_by_id(chunk_id)
    return {"message": "Chunk updated successfully", "chunk": updated_chunk}

@router.delete("/{chunk_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chunk_endpoint(chunk_id: str):
    """
    Delete a chunk by its ID.
    """
    existing_chunk = await get_chunk_by_id(chunk_id)
    if not existing_chunk:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chunk with ID {chunk_id} not found"
        )
    
    deleted_count = await delete_chunk(chunk_id)
    if deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete chunk"
        )
    
    return None
