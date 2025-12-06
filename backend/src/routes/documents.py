"""
Document management routes for the knowledge base.
"""

import logging
from fastapi import APIRouter, HTTPException

from ..models import (
    DocumentAddRequest,
    DocumentAddResponse,
    SearchRequest,
    SearchResponse,
    SearchResult
)
from ..services import rag_service, qdrant_service


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post(
    "/",
    response_model=DocumentAddResponse,
    summary="Add documents to knowledge base",
    description="Add one or more documents to the knowledge base for RAG retrieval."
)
async def add_documents(request: DocumentAddRequest) -> DocumentAddResponse:
    """
    Add documents to the knowledge base.

    - **documents**: List of documents to add (each with content, optional metadata, and optional ID)
    """
    try:
        logger.info(f"Received request to add {len(request.documents)} documents")

        # Extract document data
        documents = [doc.content for doc in request.documents]
        metadata = [doc.metadata if doc.metadata else {} for doc in request.documents]
        ids = [doc.doc_id for doc in request.documents if doc.doc_id]

        # If no IDs provided, set to None to auto-generate
        if len(ids) != len(documents):
            ids = None

        # Add documents to the knowledge base
        doc_ids = rag_service.add_documents(documents, metadata, ids)

        return DocumentAddResponse(
            success=True,
            message=f"Successfully added {len(doc_ids)} documents to the knowledge base",
            document_count=len(doc_ids),
            document_ids=doc_ids
        )

    except Exception as e:
        logger.error(f"Error adding documents: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to add documents: {str(e)}"
        )


@router.post(
    "/search",
    response_model=SearchResponse,
    summary="Search the knowledge base",
    description="Search for relevant documents in the knowledge base using semantic similarity."
)
async def search_documents(request: SearchRequest) -> SearchResponse:
    """
    Search the knowledge base for relevant documents.

    - **query**: The search query text
    - **limit**: Maximum number of results to return (1-20, default 5)
    - **min_score**: Minimum similarity score threshold (0.0-1.0, default 0.5)
    """
    try:
        logger.info(f"Received search request: {request.query[:50]}...")

        # Search the knowledge base
        results = rag_service.search_knowledge_base(
            query=request.query,
            limit=request.limit,
            min_score=request.min_score
        )

        # Format results
        search_results = [
            SearchResult(
                content=result["content"],
                score=result["score"],
                metadata=result.get("metadata", {}),
                doc_id=result["doc_id"]
            )
            for result in results
        ]

        return SearchResponse(
            query=request.query,
            results=search_results,
            count=len(search_results)
        )

    except Exception as e:
        logger.error(f"Error searching documents: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to search documents: {str(e)}"
        )


@router.delete(
    "/{doc_id}",
    summary="Delete a document",
    description="Delete a document from the knowledge base by its ID."
)
async def delete_document(doc_id: str) -> dict:
    """
    Delete a document from the knowledge base.

    - **doc_id**: The ID of the document to delete
    """
    try:
        logger.info(f"Deleting document: {doc_id}")

        success = qdrant_service.delete_documents([doc_id])

        if success:
            return {
                "success": True,
                "message": f"Document {doc_id} deleted successfully"
            }
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to delete document"
            )

    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete document: {str(e)}"
        )


@router.delete(
    "/",
    summary="Clear all documents",
    description="Delete all documents from the knowledge base."
)
async def clear_documents() -> dict:
    """
    Clear all documents from the knowledge base.
    Use with caution - this cannot be undone!
    """
    try:
        logger.info("Clearing all documents from knowledge base")

        success = qdrant_service.clear_collection()

        if success:
            return {
                "success": True,
                "message": "All documents cleared from knowledge base"
            }
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to clear documents"
            )

    except Exception as e:
        logger.error(f"Error clearing documents: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear documents: {str(e)}"
        )


@router.get(
    "/info",
    summary="Get collection information",
    description="Get information about the knowledge base collection."
)
async def get_collection_info() -> dict:
    """
    Get information about the knowledge base collection.
    """
    try:
        info = qdrant_service.get_collection_info()
        return info

    except Exception as e:
        logger.error(f"Error getting collection info: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get collection info: {str(e)}"
        )
