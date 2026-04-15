from celery import shared_task
from .services.rag_service import WeaviateRAGService
import logging

logger = logging.getLogger(__name__)


@shared_task
def indexer_document(text, file_name, user_id):
    try:
        with WeaviateRAGService() as weaviate_service:
            count = weaviate_service.index_document(text, file_name, str(user_id))
            logger.info(f"Indexed document {file_name} for user {user_id} ({count} chunks)")
            return {"success": True, "chunks_count": count}
    except Exception as e:
        logger.exception(f"Failed to index document {file_name} for user {user_id}")
        return {"success": False, "error": str(e)}
