import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks


from app.services.chunk_annotation_service import ChunkAnnotationService
from app.services.llm_service import LLMQuotaExceededError
from app.dependencies import get_annotation_service
from app.model.chunk import ChunkSchema, AnnotationStatus

router = APIRouter(
    prefix="/annotation",
    tags=["Chunk Annotation"]
)

logger = logging.getLogger(__name__)


@router.post(
    "/batch/unannotated",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=dict,
    summary="Triggers background annotation for unannotated chunks."
)
async def trigger_batch_annotation_all(
    background_tasks: BackgroundTasks,
    limit: Optional[int] = None,
    annotation_service: ChunkAnnotationService = Depends(get_annotation_service)
):
    """
    Triggers a background job that annotates unannotated/stale chunks.
    The job runs independently from the HTTP connection.
    """
    logger.info(f"Admin triggered batch annotation of unannotated chunks (limit={limit}).")

    try:
        background_tasks.add_task(annotation_service.batch_annotate_unannotated_chunks, limit=limit)
        return {
            "message": "Batch annotation process initiated in the background.",
            "status": "202 Accepted - Processing started (check server logs or monitoring endpoint for progress).",
            "action": "batch_annotate_unannotated",
            "limit": limit
        }

    except Exception as e:
        logger.exception("Failed to initiate background annotation task.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initiate batch annotation. Reason: {str(e)}"
        )


@router.post(
    "/batch/retry_failed",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=dict,
    summary="Triggers background retry for all failed annotations."
)
async def retry_failed_annotations(
    background_tasks: BackgroundTasks,
    include_quota: bool = False,
    annotation_service: ChunkAnnotationService = Depends(get_annotation_service)
):
    """
    Triggers a background job that retries annotation for all previously failed chunks.
    Use `include_quota=true` to include quota-exceeded chunks as well.
    """
    logger.info(f"Admin triggered batch retry of failed chunks (include_quota={include_quota}).")

    try:
        # Remove 'limit' argument here
        background_tasks.add_task(
            annotation_service.retry_failed_chunks,
            include_quota=include_quota
        )

        return {
            "message": "Batch retry process initiated in the background for all failed chunks.",
            "status": "202 Accepted - Processing started (check server logs or monitoring endpoint for progress).",
            "action": "batch_retry_failed",
            "include_quota": include_quota
        }

    except Exception as e:
        logger.exception("Failed to initiate retry of failed chunks.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initiate retry task. Reason: {str(e)}"
        )



@router.post(
    "/{chunk_id}",
    response_model=ChunkSchema,
    status_code=status.HTTP_200_OK,
    summary="Annotates a single chunk by ID."
)
async def annotate_chunk(
    chunk_id: str,
    annotation_service: ChunkAnnotationService = Depends(get_annotation_service)
):
    """
    Triggers annotation for a single chunk and returns the updated chunk record.
    Raises a 404 if the chunk does not exist or failed to annotate.
    """
    logger.info(f"Annotation requested for chunk ID: {chunk_id}")

    try:
        annotated_chunk = await annotation_service.annotate_single_chunk(chunk_id)

        if not annotated_chunk:
            logger.warning(f"Chunk {chunk_id} not found or annotation returned None.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Chunk ID '{chunk_id}' not found or annotation failed."
            )

        if annotated_chunk.status in [AnnotationStatus.FAILED_QUOTA, AnnotationStatus.FAILED_GEN]:
            logger.error(f"Annotation failed for chunk {chunk_id} with status {annotated_chunk.status}.")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Annotation process failed for chunk ID '{chunk_id}'. "
                       f"Status: {annotated_chunk.status.value}"
            )

        logger.info(f"Annotation completed for chunk ID: {chunk_id}")
        return annotated_chunk

    except LLMQuotaExceededError as e:
        logger.warning(f"LLM quota exceeded during annotation for chunk {chunk_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"LLM Annotation Service Quota Exceeded: {e}"
        )

    except HTTPException:
        raise  # re-raise known HTTP errors

    except Exception as e:
        logger.exception(f"Unexpected error during annotation for chunk {chunk_id}.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during annotation: {str(e)}"
        )
