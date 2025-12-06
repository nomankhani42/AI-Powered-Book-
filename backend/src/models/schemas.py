"""
Pydantic models for request and response validation.
"""

from typing import Optional
from pydantic import BaseModel, Field


# ============================================================================
# CHAT MODELS
# ============================================================================

class ChatRequest(BaseModel):
    """Request model for chat endpoint."""

    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="User's message/question",
        examples=["What is machine learning?"]
    )
    session_id: Optional[str] = Field(
        default=None,
        description="Optional session ID to maintain conversation context",
        examples=["user123_session1"]
    )
    use_rag: bool = Field(
        default=True,
        description="Whether to use RAG (retrieve context from knowledge base)"
    )


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""

    response: str = Field(
        ...,
        description="Agent's response to the user's message"
    )
    session_id: Optional[str] = Field(
        default=None,
        description="Session ID for maintaining conversation context"
    )
    sources: Optional[list[dict]] = Field(
        default=None,
        description="List of sources used to generate the response (when RAG is enabled)"
    )
    metadata: dict = Field(
        default_factory=dict,
        description="Additional metadata about the response"
    )


# ============================================================================
# DOCUMENT MODELS
# ============================================================================

class Document(BaseModel):
    """Model for a document to be indexed."""

    content: str = Field(
        ...,
        min_length=1,
        description="Document content/text"
    )
    metadata: Optional[dict] = Field(
        default=None,
        description="Optional metadata for the document (e.g., source, title, author)"
    )
    doc_id: Optional[str] = Field(
        default=None,
        description="Optional document ID (auto-generated if not provided)"
    )


class DocumentAddRequest(BaseModel):
    """Request model for adding documents to the knowledge base."""

    documents: list[Document] = Field(
        ...,
        min_length=1,
        description="List of documents to add to the knowledge base"
    )


class DocumentAddResponse(BaseModel):
    """Response model for document addition."""

    success: bool = Field(
        ...,
        description="Whether the operation was successful"
    )
    message: str = Field(
        ...,
        description="Status message"
    )
    document_count: int = Field(
        ...,
        description="Number of documents successfully added"
    )
    document_ids: list[str] = Field(
        default_factory=list,
        description="IDs of the added documents"
    )


class SearchRequest(BaseModel):
    """Request model for searching the knowledge base."""

    query: str = Field(
        ...,
        min_length=1,
        description="Search query"
    )
    limit: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Maximum number of results to return"
    )
    min_score: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Minimum similarity score threshold"
    )


class SearchResult(BaseModel):
    """Model for a single search result."""

    content: str = Field(
        ...,
        description="Document content"
    )
    score: float = Field(
        ...,
        description="Similarity score (0.0 to 1.0)"
    )
    metadata: Optional[dict] = Field(
        default=None,
        description="Document metadata"
    )
    doc_id: str = Field(
        ...,
        description="Document ID"
    )


class SearchResponse(BaseModel):
    """Response model for search endpoint."""

    query: str = Field(
        ...,
        description="Original search query"
    )
    results: list[SearchResult] = Field(
        default_factory=list,
        description="List of matching documents"
    )
    count: int = Field(
        ...,
        description="Number of results returned"
    )


# ============================================================================
# HEALTH CHECK MODELS
# ============================================================================

class HealthResponse(BaseModel):
    """Response model for health check endpoint."""

    status: str = Field(
        ...,
        description="Service status"
    )
    version: str = Field(
        ...,
        description="API version"
    )
    qdrant_connected: bool = Field(
        ...,
        description="Whether Qdrant is connected and accessible"
    )
    collection_exists: bool = Field(
        ...,
        description="Whether the collection exists in Qdrant"
    )
