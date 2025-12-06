"""
Application configuration settings using Pydantic Settings.
Automatically loads environment variables from .env file.
"""

from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # ========================================================================
    # GEMINI API CONFIGURATION
    # ========================================================================
    gemini_api_key: str = Field(
        ...,
        description="Gemini API key from https://aistudio.google.com/apikey"
    )
    gemini_model: str = Field(
        default="gemini/gemini-2.0-flash",
        description="Gemini model name (e.g., gemini/gemini-2.0-flash)"
    )

    # ========================================================================
    # QDRANT CONFIGURATION
    # ========================================================================
    qdrant_mode: Literal["local", "local-persistent", "remote"] = Field(
        default="remote",
        description="Qdrant operation mode"
    )
    qdrant_path: str = Field(
        default="./qdrant_data",
        description="Path for local persistent storage"
    )
    qdrant_url: str = Field(
        default="http://localhost:6333",
        description="Qdrant server URL for remote mode"
    )
    qdrant_api_key: str | None = Field(
        default=None,
        description="Qdrant Cloud API key (optional)"
    )
    qdrant_collection_name: str = Field(
        default="chatbot_documents",
        description="Collection name for storing embeddings"
    )
    vector_size: int = Field(
        default=384,
        description="Vector dimension size (must match embedding model)"
    )

    # ========================================================================
    # EMBEDDING MODEL CONFIGURATION
    # ========================================================================
    embedding_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        description="Model for text embeddings"
    )

    # ========================================================================
    # FASTAPI APPLICATION CONFIGURATION
    # ========================================================================
    app_title: str = Field(
        default="RAG Chatbot API",
        description="Application title"
    )
    app_version: str = Field(
        default="1.0.0",
        description="Application version"
    )
    app_description: str = Field(
        default="A RAG-powered chatbot API using FastAPI, OpenAI Agents SDK, Gemini, and Qdrant",
        description="Application description"
    )
    host: str = Field(
        default="0.0.0.0",
        description="Server host"
    )
    port: int = Field(
        default=8000,
        description="Server port"
    )
    environment: Literal["development", "staging", "production"] = Field(
        default="development",
        description="Application environment"
    )
    debug: bool = Field(
        default=True,
        description="Enable debug mode"
    )
    cors_enabled: bool = Field(
        default=True,
        description="Enable CORS"
    )
    cors_origins: str = Field(
        default="http://localhost:3000,http://localhost:5173",
        description="Comma-separated list of allowed CORS origins"
    )

    # ========================================================================
    # AGENT CONFIGURATION
    # ========================================================================
    agent_name: str = Field(
        default="RAG Assistant",
        description="Default agent name"
    )
    agent_instructions: str = Field(
        default="You are a helpful AI assistant with access to a knowledge base. Use the provided context to answer questions accurately. If you don't know the answer, say so.",
        description="Agent system prompt"
    )
    max_search_results: int = Field(
        default=5,
        description="Maximum number of search results from Qdrant"
    )
    min_similarity_score: float = Field(
        default=0.5,
        description="Minimum similarity score for search results (0.0 to 1.0)"
    )

    # ========================================================================
    # LOGGING CONFIGURATION
    # ========================================================================
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        description="Logging level"
    )

    # ========================================================================
    # MODEL CONFIGURATION
    # ========================================================================
    model_temperature: float = Field(
        default=0.7,
        description="Temperature for model responses (0.0 to 1.0)"
    )
    model_max_tokens: int = Field(
        default=1000,
        description="Maximum tokens in response"
    )

    # ========================================================================
    # TRACING CONFIGURATION
    # ========================================================================
    disable_tracing: bool = Field(
        default=True,
        description="Disable OpenAI Agents SDK tracing (recommended for non-OpenAI models like Gemini)"
    )
    tracing_export_api_key: str | None = Field(
        default=None,
        description="Optional OpenAI API key for exporting traces (only if disable_tracing=False)"
    )

    # Pydantic settings configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


# Global settings instance
settings = Settings()
