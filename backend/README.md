# RAG Chatbot Backend

A production-ready RAG (Retrieval-Augmented Generation) chatbot backend built with FastAPI, OpenAI Agents SDK, Google Gemini, and Qdrant vector database.

## Features

- **RAG Architecture**: Combines vector search with LLM generation for accurate, context-aware responses
- **Google Gemini Integration**: Uses Gemini models via LiteLLM for powerful language understanding
- **Vector Database**: Qdrant for efficient semantic search and document retrieval
- **OpenAI Agents SDK**: Leverages agents, tools, and handoffs for sophisticated workflows
- **FastAPI Backend**: Modern, fast, and production-ready API framework
- **Automatic Embeddings**: Uses fastembed for automatic document vectorization
- **Flexible Configuration**: Environment-based configuration with comprehensive settings
- **CORS Support**: Ready for frontend integration

## Architecture

```
┌─────────────┐
│   Frontend  │
└──────┬──────┘
       │ HTTP/REST
       ▼
┌─────────────────────────────────────────┐
│           FastAPI Application           │
├─────────────────────────────────────────┤
│  Routes: /chat, /documents, /health     │
└──────────────┬──────────────────────────┘
               │
       ┌───────┴────────┐
       ▼                ▼
┌──────────────┐  ┌──────────────┐
│  RAG Service │  │Qdrant Service│
├──────────────┤  ├──────────────┤
│ OpenAI Agents│  │Vector Storage│
│ + Gemini LLM │  │  + Search    │
└──────────────┘  └──────────────┘
```

## Prerequisites

- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Google Gemini API key ([Get it here](https://aistudio.google.com/apikey))
- Docker and Docker Compose (for Qdrant server) - [Install Docker](https://docs.docker.com/get-docker/)

## Installation

### 1. Clone and navigate to backend

```bash
cd backend
```

### 2. Install dependencies with uv

```bash
# Install all dependencies
uv sync
```

Or install manually:

```bash
# Install main dependencies
uv add fastapi uvicorn openai-agents qdrant-client python-dotenv pydantic pydantic-settings

# Install LiteLLM support for Gemini
uv add "openai-agents[litellm]"
```

### 3. Start Qdrant Server

Start Qdrant using Docker Compose:

```bash
# Start Qdrant in the background
docker-compose up -d

# Verify it's running
curl http://localhost:6333/health
```

This starts:
- **Qdrant REST API** on port 6333
- **Qdrant Web UI** on port 6335 (optional dashboard)

**See [QDRANT_SETUP.md](QDRANT_SETUP.md) for alternative setups (Qdrant Cloud, etc.)**

### 4. Configure environment variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your configuration:

```env
# Required: Get from https://aistudio.google.com/apikey
GEMINI_API_KEY=your_gemini_api_key_here

# Qdrant configuration (Docker setup)
QDRANT_MODE=remote
QDRANT_URL=http://localhost:6333

# Other settings (optional, defaults provided)
GEMINI_MODEL=gemini/gemini-2.0-flash
QDRANT_COLLECTION_NAME=chatbot_documents
```

## Environment Variables Documentation

### Required Variables

| Variable | Description | Where to Get |
|----------|-------------|--------------|
| `GEMINI_API_KEY` | Your Gemini API key | [Get from Google AI Studio](https://aistudio.google.com/apikey) |

### Qdrant Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `QDRANT_MODE` | `local` | Mode: `local` (in-memory), `local-persistent` (disk), or `remote` |
| `QDRANT_PATH` | `./qdrant_data` | Path for local persistent storage |
| `QDRANT_URL` | `http://localhost:6333` | URL for remote Qdrant server |
| `QDRANT_API_KEY` | - | API key for Qdrant Cloud ([Get it here](https://cloud.qdrant.io/)) |
| `QDRANT_COLLECTION_NAME` | `chatbot_documents` | Collection name for storing embeddings |
| `VECTOR_SIZE` | `384` | Vector dimension (must match embedding model) |

### Model Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `GEMINI_MODEL` | `gemini/gemini-2.0-flash` | Gemini model to use |
| `EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | Model for text embeddings |
| `MODEL_TEMPERATURE` | `0.7` | Response creativity (0.0-1.0) |
| `MODEL_MAX_TOKENS` | `1000` | Maximum response length |

### Application Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_TITLE` | `RAG Chatbot API` | API title |
| `APP_VERSION` | `1.0.0` | API version |
| `HOST` | `0.0.0.0` | Server host |
| `PORT` | `8000` | Server port |
| `ENVIRONMENT` | `development` | Environment: development, staging, production |
| `DEBUG` | `true` | Enable debug mode |
| `CORS_ENABLED` | `true` | Enable CORS |
| `CORS_ORIGINS` | `http://localhost:3000,...` | Allowed CORS origins (comma-separated) |

### Agent Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `AGENT_NAME` | `RAG Assistant` | Agent name |
| `AGENT_INSTRUCTIONS` | (see `.env.example`) | System prompt for agent |
| `MAX_SEARCH_RESULTS` | `5` | Max results from vector search |
| `MIN_SIMILARITY_SCORE` | `0.5` | Minimum similarity threshold (0.0-1.0) |

### Tracing Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `DISABLE_TRACING` | `true` | **Disable tracing (recommended for Gemini)**. Set to `false` only if using OpenAI models |
| `TRACING_EXPORT_API_KEY` | - | OpenAI API key for traces (only if `DISABLE_TRACING=false`) |

**Important**: When using Gemini or other non-OpenAI models via LiteLLM, keep `DISABLE_TRACING=true` to avoid errors. The OpenAI Agents SDK's tracing feature is designed for OpenAI models only.

## Running the Application

### Development Mode

```bash
# Using uv
uv run python run.py

# Or activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
python run.py
```

### Production Mode

```bash
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at:
- Main API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Health Check

#### GET `/health`
Check API health status

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "qdrant_connected": true,
  "collection_exists": true
}
```

### Chat

#### POST `/chat`
Send a message to the chatbot

**Request:**
```json
{
  "message": "What is machine learning?",
  "session_id": "user123_session1",
  "use_rag": true
}
```

**Response:**
```json
{
  "response": "Machine learning is...",
  "session_id": "user123_session1",
  "sources": [
    {
      "content": "Document excerpt...",
      "score": 0.85,
      "doc_id": "abc123",
      "metadata": {}
    }
  ],
  "metadata": {
    "use_rag": true,
    "model": "gemini/gemini-2.0-flash",
    "usage": {
      "total_tokens": 150,
      "prompt_tokens": 100,
      "completion_tokens": 50
    }
  }
}
```

### Document Management

#### POST `/documents`
Add documents to the knowledge base

**Request:**
```json
{
  "documents": [
    {
      "content": "Machine learning is a subset of AI...",
      "metadata": {
        "source": "ML Textbook",
        "chapter": "Introduction"
      },
      "doc_id": "ml_intro_1"
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully added 1 documents to the knowledge base",
  "document_count": 1,
  "document_ids": ["ml_intro_1"]
}
```

#### POST `/documents/search`
Search the knowledge base

**Request:**
```json
{
  "query": "What is machine learning?",
  "limit": 5,
  "min_score": 0.5
}
```

**Response:**
```json
{
  "query": "What is machine learning?",
  "results": [
    {
      "content": "Machine learning is...",
      "score": 0.92,
      "metadata": {},
      "doc_id": "ml_intro_1"
    }
  ],
  "count": 1
}
```

#### DELETE `/documents/{doc_id}`
Delete a specific document

#### DELETE `/documents`
Clear all documents (use with caution!)

#### GET `/documents/info`
Get collection information

## Project Structure

```
backend/
├── src/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py      # Configuration settings
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py       # Pydantic models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── chat.py          # Chat endpoints
│   │   ├── documents.py     # Document management
│   │   └── health.py        # Health check
│   └── services/
│       ├── __init__.py
│       ├── qdrant_service.py # Qdrant operations
│       └── rag_service.py    # RAG logic with Gemini
├── .env.example             # Environment template
├── .env                     # Your configuration (gitignored)
├── .gitignore
├── pyproject.toml          # UV project configuration
├── uv.lock                 # Dependency lock file
├── run.py                  # Run script
└── README.md               # This file
```

## Usage Examples

### Python Client Example

```python
import requests

# Base URL
BASE_URL = "http://localhost:8000"

# Add documents to knowledge base
documents = {
    "documents": [
        {
            "content": "Python is a high-level programming language.",
            "metadata": {"topic": "programming"}
        },
        {
            "content": "Machine learning is a branch of AI.",
            "metadata": {"topic": "AI"}
        }
    ]
}

response = requests.post(f"{BASE_URL}/documents", json=documents)
print(response.json())

# Chat with RAG
chat_request = {
    "message": "What is Python?",
    "use_rag": True
}

response = requests.post(f"{BASE_URL}/chat", json=chat_request)
result = response.json()
print(f"Response: {result['response']}")
print(f"Sources: {result['sources']}")
```

### cURL Examples

```bash
# Health check
curl http://localhost:8000/health

# Add document
curl -X POST http://localhost:8000/documents \
  -H "Content-Type: application/json" \
  -d '{
    "documents": [{
      "content": "FastAPI is a modern web framework.",
      "metadata": {"topic": "web"}
    }]
  }'

# Chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tell me about FastAPI",
    "use_rag": true
  }'

# Search
curl -X POST http://localhost:8000/documents/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "web framework",
    "limit": 5
  }'
```

## Qdrant Setup Options

> **💡 See [QDRANT_SETUP.md](QDRANT_SETUP.md) for detailed setup instructions**

### Option 1: Self-Hosted with Docker (Recommended for Development)

```bash
# Start Qdrant server
docker-compose up -d

# Verify it's running
curl http://localhost:6333/health
```

**Configuration:**
```env
QDRANT_MODE=remote
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=  # Leave empty
```

✅ Persistent storage
✅ Web UI at http://localhost:6335
✅ Easy to manage with docker-compose

### Option 2: Qdrant Cloud (Recommended for Production)

1. Sign up at [https://cloud.qdrant.io/](https://cloud.qdrant.io/)
2. Create a cluster (free tier available)
3. Get your cluster URL and API key

**Configuration:**
```env
QDRANT_MODE=remote
QDRANT_URL=https://your-cluster.cloud.qdrant.io:6333
QDRANT_API_KEY=your_qdrant_api_key
```

✅ Fully managed
✅ Auto-scaling
✅ Daily backups
✅ Global availability

### Option 3: Local Modes (For Testing Only)

**In-Memory (not persisted):**
```env
QDRANT_MODE=local
```

**Local Persistent:**
```env
QDRANT_MODE=local-persistent
QDRANT_PATH=./qdrant_data
```

## Available Gemini Models

Configure via `GEMINI_MODEL` environment variable:

- `gemini/gemini-2.0-flash` - Fast, efficient (recommended)
- `gemini/gemini-1.5-pro` - More powerful, slower
- `gemini/gemini-1.5-flash` - Older fast model

## Troubleshooting

### "Failed to initialize Qdrant client"
- Check `QDRANT_MODE` is set correctly
- For remote mode, verify `QDRANT_URL` and `QDRANT_API_KEY`
- Ensure Qdrant service is running

### "API key not found"
- Make sure `.env` file exists
- Verify `GEMINI_API_KEY` is set
- Check the key is valid at [Google AI Studio](https://aistudio.google.com/apikey)

### CORS errors
- Add your frontend URL to `CORS_ORIGINS` in `.env`
- Format: `http://localhost:3000,http://localhost:5173`

### Import errors
- Ensure you're in the virtual environment: `source .venv/bin/activate`
- Or use `uv run` prefix: `uv run python run.py`

## Development

### Running Tests
```bash
# TODO: Add tests
uv run pytest
```

### Code Formatting
```bash
# Install dev dependencies
uv add --dev black isort

# Format code
uv run black src/
uv run isort src/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License

## Support

For issues and questions:
- Create an issue in the repository
- Check the [OpenAI Agents SDK docs](https://openai.github.io/openai-agents-python/)
- Check [Qdrant documentation](https://qdrant.tech/documentation/)
- Check [FastAPI documentation](https://fastapi.tiangolo.com/)

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Powered by [OpenAI Agents SDK](https://github.com/openai/openai-agents-python)
- Uses [Google Gemini](https://ai.google.dev/)
- Vector database by [Qdrant](https://qdrant.tech/)
- Package management by [uv](https://docs.astral.sh/uv/)
