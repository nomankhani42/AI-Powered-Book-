"""
Qdrant service for vector storage and similarity search.
Handles document embeddings and retrieval.
"""

import logging
import uuid
from typing import Optional

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from ..config import settings


logger = logging.getLogger(__name__)


class QdrantService:
    """Service for interacting with Qdrant vector database."""

    def __init__(self):
        """Initialize Qdrant client based on configuration."""
        self.client: Optional[QdrantClient] = None
        self.collection_name = settings.qdrant_collection_name
        self.embedding_model = settings.embedding_model
        self._initialize_client()
        self._set_embedding_model()

    def _initialize_client(self):
        """Initialize Qdrant client based on mode (local, persistent, or remote)."""
        try:
            if settings.qdrant_mode == "local":
                # In-memory mode (data not persisted)
                logger.info("Initializing Qdrant in local in-memory mode")
                self.client = QdrantClient(":memory:")

            elif settings.qdrant_mode == "local-persistent":
                # Local persistent mode (data saved to disk)
                logger.info(f"Initializing Qdrant in local persistent mode: {settings.qdrant_path}")
                self.client = QdrantClient(path=settings.qdrant_path)

            elif settings.qdrant_mode == "remote":
                # Remote server mode (Qdrant Cloud or self-hosted)
                logger.info(f"Initializing Qdrant in remote mode: {settings.qdrant_url}")
                self.client = QdrantClient(
                    url=settings.qdrant_url,
                    api_key=settings.qdrant_api_key
                )

            else:
                raise ValueError(f"Invalid QDRANT_MODE: {settings.qdrant_mode}")

            # Initialize collection
            self._initialize_collection()

            logger.info("Qdrant client initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize Qdrant client: {e}")
            raise

    def _initialize_collection(self):
        """Check if collection exists - fastembed will create it on first add."""
        try:
            if self.client.collection_exists(self.collection_name):
                logger.info(f"Collection '{self.collection_name}' already exists")
            else:
                # Don't create manually - fastembed will create with correct params
                # when documents are added via client.add()
                logger.info(f"Collection '{self.collection_name}' does not exist yet. Will be created on first document add.")

        except Exception as e:
            logger.error(f"Failed to check collection: {e}")
            raise

    def _set_embedding_model(self):
        """Set the embedding model for fastembed."""
        # Using fastembed's default model (BAAI/bge-small-en-v1.5, 384 dims)
        # This is handled automatically by qdrant-client[fastembed]
        logger.info(f"Using fastembed default embedding model")

    def add_documents(
        self,
        documents: list[str],
        metadata: Optional[list[dict]] = None,
        ids: Optional[list[str]] = None
    ) -> list[str]:
        """
        Add documents to the collection with automatic embedding.

        Args:
            documents: List of document texts to add
            metadata: Optional list of metadata dicts for each document
            ids: Optional list of document IDs (auto-generated if not provided)

        Returns:
            List of document IDs
        """
        try:
            # Generate IDs if not provided
            if ids is None:
                ids = [str(uuid.uuid4()) for _ in documents]

            # Prepare metadata
            if metadata is None:
                metadata = [{} for _ in documents]

            # Ensure metadata includes the document ID
            for i, meta in enumerate(metadata):
                meta["doc_id"] = ids[i]

            logger.info(f"Adding {len(documents)} documents to collection '{self.collection_name}'")

            # Use Qdrant's add method with automatic embedding via fastembed
            # Note: This requires qdrant-client[fastembed] to be installed
            # Model is set via set_model() in _set_embedding_model()
            self.client.add(
                collection_name=self.collection_name,
                documents=documents,
                metadata=metadata,
                ids=ids
            )

            logger.info(f"Successfully added {len(documents)} documents")
            return ids

        except Exception as e:
            logger.error(f"Failed to add documents: {e}")
            raise

    def search_documents(
        self,
        query: str,
        limit: int = 5,
        min_score: float = 0.5
    ) -> list[dict]:
        """
        Search for similar documents using text query.

        Args:
            query: Search query text
            limit: Maximum number of results to return
            min_score: Minimum similarity score threshold (0.0 to 1.0)

        Returns:
            List of matching documents with scores and metadata
        """
        try:
            logger.info(f"Searching for: '{query}' (limit={limit}, min_score={min_score})")

            # Use Qdrant's query method with automatic embedding
            # Model is set via set_model() in _set_embedding_model()
            results = self.client.query(
                collection_name=self.collection_name,
                query_text=query,
                limit=limit
            )

            # Filter by minimum score and format results
            formatted_results = []
            for result in results:
                # Qdrant returns scores in different ways depending on distance metric
                # For COSINE distance, higher is better (range 0 to 1)
                score = getattr(result, 'score', 0.0)

                if score >= min_score:
                    formatted_results.append({
                        "content": result.document if hasattr(result, 'document') else "",
                        "score": float(score),
                        "metadata": result.metadata if hasattr(result, 'metadata') else {},
                        "doc_id": result.id if hasattr(result, 'id') else result.metadata.get('doc_id', 'unknown')
                    })

            logger.info(f"Found {len(formatted_results)} documents above threshold")
            return formatted_results

        except Exception as e:
            logger.error(f"Failed to search documents: {e}")
            raise

    def delete_documents(self, ids: list[str]) -> bool:
        """
        Delete documents by their IDs.

        Args:
            ids: List of document IDs to delete

        Returns:
            True if successful
        """
        try:
            logger.info(f"Deleting {len(ids)} documents")

            self.client.delete(
                collection_name=self.collection_name,
                points_selector=ids
            )

            logger.info(f"Successfully deleted {len(ids)} documents")
            return True

        except Exception as e:
            logger.error(f"Failed to delete documents: {e}")
            raise

    def clear_collection(self) -> bool:
        """
        Delete the collection (will be recreated by fastembed on next add).

        Returns:
            True if successful
        """
        try:
            logger.info(f"Clearing collection '{self.collection_name}'")

            if self.client.collection_exists(self.collection_name):
                self.client.delete_collection(self.collection_name)
                logger.info("Collection deleted successfully. Will be recreated on next document add.")
            else:
                logger.info("Collection does not exist, nothing to clear.")

            return True

        except Exception as e:
            logger.error(f"Failed to clear collection: {e}")
            raise

    def recreate_collection(self) -> bool:
        """
        Delete the collection so fastembed can recreate it with correct parameters.
        Use this when vector dimensions mismatch.

        Returns:
            True if successful
        """
        try:
            logger.info(f"Deleting collection '{self.collection_name}' for recreation by fastembed")

            # Delete existing collection if it exists
            if self.client.collection_exists(self.collection_name):
                self.client.delete_collection(self.collection_name)
                logger.info(f"Deleted existing collection '{self.collection_name}'")

            # Don't create manually - let fastembed create it with correct params
            # when documents are added via client.add()

            logger.info(f"Collection '{self.collection_name}' deleted. Will be recreated on first document add.")
            return True

        except Exception as e:
            logger.error(f"Failed to delete collection: {e}")
            raise

    def get_collection_info(self) -> dict:
        """
        Get information about the collection.

        Returns:
            Dictionary with collection information
        """
        try:
            info = self.client.get_collection(self.collection_name)
            return {
                "name": self.collection_name,
                "vectors_count": info.vectors_count,
                "points_count": info.points_count,
                "status": info.status.value if hasattr(info.status, 'value') else str(info.status)
            }

        except Exception as e:
            logger.error(f"Failed to get collection info: {e}")
            raise

    def health_check(self) -> dict:
        """
        Check if Qdrant is healthy and accessible.

        Returns:
            Dictionary with health status
        """
        try:
            # Check if client is initialized
            if self.client is None:
                return {
                    "connected": False,
                    "collection_exists": False,
                    "error": "Client not initialized"
                }

            # Check if collection exists
            collection_exists = self.client.collection_exists(self.collection_name)

            return {
                "connected": True,
                "collection_exists": collection_exists,
                "collection_name": self.collection_name
            }

        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                "connected": False,
                "collection_exists": False,
                "error": str(e)
            }


# Global instance
qdrant_service = QdrantService()
