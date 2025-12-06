"""
RAG (Retrieval-Augmented Generation) service using OpenAI Agents SDK with Gemini.
Combines vector search with LLM-based generation for context-aware responses.
"""

import logging
from typing import Optional

from agents import Agent, Runner, function_tool, ModelSettings, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel

from ..config import settings
from .qdrant_service import qdrant_service


logger = logging.getLogger(__name__)

# Configure tracing based on settings
# Tracing is disabled by default for non-OpenAI models (Gemini)
# Enable it only if you have an OpenAI API key for tracing purposes
if settings.disable_tracing:
    set_tracing_disabled(disabled=True)
    logger.info("Tracing disabled (recommended for Gemini/LiteLLM)")
else:
    if settings.tracing_export_api_key:
        from agents import set_tracing_export_api_key
        set_tracing_export_api_key(settings.tracing_export_api_key)
        logger.info("Tracing enabled with export API key")
    else:
        logger.warning("Tracing not disabled but no export API key provided - may cause issues with non-OpenAI models")


class RAGService:
    """Service for RAG-powered chatbot using OpenAI Agents SDK with Gemini."""

    def __init__(self):
        """Initialize the RAG service with Gemini model and Qdrant."""
        self.qdrant = qdrant_service
        self._initialize_agent()

    def _initialize_agent(self):
        """Initialize the AI agent with Gemini model and RAG tools."""
        try:
            logger.info(f"Initializing agent with model: {settings.gemini_model}")

            # Create LiteLLM model for Gemini
            gemini_model = LitellmModel(
                model=settings.gemini_model,
                api_key=settings.gemini_api_key
            )

            # Define the knowledge base search tool
            @function_tool
            def search_knowledge_base(query: str) -> str:
                """
                Search the knowledge base for relevant information.
                Use this tool when you need to find information to answer the user's question.

                Args:
                    query: The search query to find relevant documents

                Returns:
                    Relevant context from the knowledge base
                """
                logger.info(f"Tool called: search_knowledge_base with query: '{query}'")

                try:
                    results = self.qdrant.search_documents(
                        query=query,
                        limit=settings.max_search_results,
                        min_score=settings.min_similarity_score
                    )

                    if not results:
                        return "No relevant information found in the knowledge base."

                    # Format results as context
                    context_parts = []
                    for i, result in enumerate(results, 1):
                        context_parts.append(
                            f"[Source {i}] (Score: {result['score']:.2f})\n{result['content']}"
                        )

                    context = "\n\n".join(context_parts)
                    logger.info(f"Found {len(results)} relevant documents")
                    return context

                except Exception as e:
                    logger.error(f"Error searching knowledge base: {e}")
                    return f"Error searching knowledge base: {str(e)}"

            # Create the agent with the search tool
            self.agent = Agent(
                name=settings.agent_name,
                instructions=settings.agent_instructions,
                model=gemini_model,
                model_settings=ModelSettings(
                    temperature=settings.model_temperature,
                    max_tokens=settings.model_max_tokens,
                    include_usage=True  # Track token usage
                ),
                tools=[search_knowledge_base]
            )

            # Create agent without RAG (for non-RAG queries)
            self.agent_no_rag = Agent(
                name=settings.agent_name,
                instructions=settings.agent_instructions,
                model=gemini_model,
                model_settings=ModelSettings(
                    temperature=settings.model_temperature,
                    max_tokens=settings.model_max_tokens,
                    include_usage=True
                ),
                tools=[]  # No tools for direct responses
            )

            logger.info("Agent initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize agent: {e}")
            raise

    async def chat(
        self,
        message: str,
        use_rag: bool = True,
        session_id: Optional[str] = None
    ) -> dict:
        """
        Process a chat message and generate a response.

        Args:
            message: User's message/question
            use_rag: Whether to use RAG (retrieve from knowledge base)
            session_id: Optional session ID for conversation context

        Returns:
            Dictionary with response, sources, and metadata
        """
        try:
            logger.info(f"Processing chat message (use_rag={use_rag}, session_id={session_id})")

            # Choose agent based on RAG preference
            agent = self.agent if use_rag else self.agent_no_rag

            # Run the agent
            result = await Runner.run(agent, message)

            # Extract response
            response_text = result.final_output

            # Extract sources if RAG was used
            sources = []
            if use_rag:
                # Check if the agent used the search tool
                for item in result.new_items:
                    if hasattr(item, 'tool_name') and item.tool_name == 'search_knowledge_base':
                        # Tool was called, search for the same query to get sources
                        try:
                            tool_input = getattr(item, 'input', {})
                            search_query = tool_input.get('query', message)

                            search_results = self.qdrant.search_documents(
                                query=search_query,
                                limit=settings.max_search_results,
                                min_score=settings.min_similarity_score
                            )

                            sources = [
                                {
                                    "content": r["content"][:200] + "..." if len(r["content"]) > 200 else r["content"],
                                    "score": r["score"],
                                    "doc_id": r["doc_id"],
                                    "metadata": r["metadata"]
                                }
                                for r in search_results
                            ]
                        except Exception as e:
                            logger.warning(f"Failed to extract sources: {e}")

            # Get usage statistics if available
            usage = {}
            if hasattr(result, 'context_wrapper') and hasattr(result.context_wrapper, 'usage'):
                usage_obj = result.context_wrapper.usage
                usage = {
                    "total_tokens": getattr(usage_obj, 'total_tokens', 0),
                    "prompt_tokens": getattr(usage_obj, 'prompt_tokens', 0),
                    "completion_tokens": getattr(usage_obj, 'completion_tokens', 0)
                }

            return {
                "response": response_text,
                "sources": sources if sources else None,
                "session_id": session_id,
                "metadata": {
                    "use_rag": use_rag,
                    "model": settings.gemini_model,
                    "usage": usage
                }
            }

        except Exception as e:
            logger.error(f"Error processing chat message: {e}")
            raise

    def add_documents(
        self,
        documents: list[str],
        metadata: Optional[list[dict]] = None,
        ids: Optional[list[str]] = None
    ) -> list[str]:
        """
        Add documents to the knowledge base.

        Args:
            documents: List of document texts
            metadata: Optional metadata for each document
            ids: Optional document IDs

        Returns:
            List of document IDs
        """
        try:
            logger.info(f"Adding {len(documents)} documents to knowledge base")
            return self.qdrant.add_documents(documents, metadata, ids)

        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            raise

    def search_knowledge_base(
        self,
        query: str,
        limit: int = 5,
        min_score: float = 0.5
    ) -> list[dict]:
        """
        Search the knowledge base.

        Args:
            query: Search query
            limit: Maximum number of results
            min_score: Minimum similarity score

        Returns:
            List of matching documents
        """
        try:
            logger.info(f"Searching knowledge base: '{query}'")
            return self.qdrant.search_documents(query, limit, min_score)

        except Exception as e:
            logger.error(f"Error searching knowledge base: {e}")
            raise


# Global instance
rag_service = RAGService()
