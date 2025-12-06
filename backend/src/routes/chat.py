"""
Chat routes for the RAG chatbot API.
"""

import logging
from fastapi import APIRouter, HTTPException

from ..models import ChatRequest, ChatResponse
from ..services import rag_service


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post(
    "/",
    response_model=ChatResponse,
    summary="Send a chat message",
    description="Send a message to the chatbot and receive a response. Optionally uses RAG to retrieve relevant context from the knowledge base."
)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Process a chat message and generate a response.

    - **message**: The user's message/question (required)
    - **session_id**: Optional session ID to maintain conversation context
    - **use_rag**: Whether to use RAG (retrieve context from knowledge base), default is True
    """
    try:
        logger.info(f"Received chat request: {request.message[:50]}...")

        # Process the message through the RAG service
        result = await rag_service.chat(
            message=request.message,
            use_rag=request.use_rag,
            session_id=request.session_id
        )

        return ChatResponse(
            response=result["response"],
            session_id=result["session_id"],
            sources=result["sources"],
            metadata=result["metadata"]
        )

    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process chat request: {str(e)}"
        )
