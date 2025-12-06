# Technical Documentation

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Component Details](#component-details)
3. [Data Flow](#data-flow)
4. [Configuration Guide](#configuration-guide)
5. [Deployment Guide](#deployment-guide)
6. [API Reference](#api-reference)
7. [Development Guide](#development-guide)

---

## Architecture Overview

### System Architecture

The RAG Chatbot Backend follows a layered architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                     Presentation Layer                       │
│                    (FastAPI Routes)                          │
│  /health  |  /chat  |  /documents  |  /documents/search    │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────┴────────────────────────────────────┐
│                     Business Logic Layer                     │
│                                                              │
│  ┌──────────────────┐              ┌──────────────────┐   │
│  │   RAG Service    │              │  Qdrant Service  │   │
│  │                  │              │                  │   │
│  │ - Agent mgmt     │◄────────────►│ - Vector ops     │   │
│  │ - Tool calling   │              │ - Search         │   │
│  │ - Context mgmt   │              │ - Embeddings     │   │
│  └──────────────────┘              └──────────────────┘   │
│           │                                  │              │
└───────────┼──────────────────────────────────┼──────────────┘
            │                                  │
┌───────────┴──────────────┐      ┌───────────┴──────────────┐
│   External Services      │      │   Data Layer             │
│                          │      │                          │
│  ┌──────────────────┐   │      │  ┌──────────────────┐   │
│  │  Gemini API      │   │      │  │  Qdrant DB       │   │
│  │  (via LiteLLM)   │   │      │  │  (Vectors)       │   │
│  └──────────────────┘   │      │  └──────────────────┘   │
└──────────────────────────┘      └──────────────────────────┘
```

### Key Components

1. **FastAPI Application** (`src/main.py`)
   - HTTP server and routing
   - CORS middleware
   - Request/response validation
   - Lifecycle management

2. **Configuration** (`src/config/settings.py`)
   - Environment-based settings
   - Pydantic validation
   - Type safety

3. **Models** (`src/models/schemas.py`)
   - Request/response schemas
   - Data validation
   - OpenAPI documentation

4. **Services**
   - **RAG Service** (`src/services/rag_service.py`)
     - Agent initialization
     - LLM integration (Gemini)
     - Tool management
     - Response generation

   - **Qdrant Service** (`src/services/qdrant_service.py`)
     - Vector database operations
     - Document embedding
     - Similarity search
     - Collection management

5. **Routes** (`src/routes/`)
   - API endpoint definitions
   - Request handling
   - Error management

---

## Component Details

### RAG Service

#### Responsibilities
- Initialize and manage AI agents
- Handle chat requests with RAG
- Integrate with Gemini via LiteLLM
- Manage conversation context
- Execute tool calls

#### Key Methods

```python
async def chat(message: str, use_rag: bool, session_id: Optional[str]) -> dict
```
Process a chat message and return a response with optional RAG.

```python
def add_documents(documents: list[str], metadata: list[dict], ids: list[str]) -> list[str]
```
Add documents to the knowledge base.

```python
def search_knowledge_base(query: str, limit: int, min_score: float) -> list[dict]
```
Search for relevant documents.

#### Agent Configuration

The RAG service uses two agents:

1. **RAG-Enabled Agent** (with search tool)
   - Has access to `search_knowledge_base` tool
   - Automatically retrieves context when needed
   - Used when `use_rag=True`

2. **Direct Response Agent** (no tools)
   - Responds without RAG
   - Faster for general queries
   - Used when `use_rag=False`

#### Tool Function

```python
@function_tool
def search_knowledge_base(query: str) -> str:
    """Search the knowledge base for relevant information."""
```

This tool is automatically called by the agent when it needs context to answer a question.

### Qdrant Service

#### Responsibilities
- Initialize Qdrant client
- Manage vector collections
- Embed and store documents
- Perform similarity search
- Health monitoring

#### Connection Modes

1. **Local In-Memory** (`:memory:`)
   - No persistence
   - Fast
   - Development only

2. **Local Persistent** (file path)
   - Data saved to disk
   - Survives restarts
   - Production-ready

3. **Remote** (URL + API key)
   - Qdrant Cloud or self-hosted
   - Scalable
   - Production-ready

#### Embedding Strategy

The service uses Qdrant's built-in fastembed integration:

```python
client.add(
    collection_name=collection_name,
    documents=documents,  # Plain text
    metadata=metadata,
    ids=ids
)
```

Embeddings are generated automatically using the configured model (default: `sentence-transformers/all-MiniLM-L6-v2`).

#### Search Algorithm

```python
results = client.query(
    collection_name=collection_name,
    query_text=query,  # Plain text query
    limit=limit
)
```

Uses COSINE similarity for semantic matching.

---

## Data Flow

### Chat Request Flow (with RAG)

```
1. User sends message
   ↓
2. FastAPI receives POST /chat
   ↓
3. Request validated (Pydantic)
   ↓
4. RAG Service receives message
   ↓
5. Agent processes message
   ↓
6. Agent decides to call search_knowledge_base tool
   ↓
7. Tool queries Qdrant Service
   ↓
8. Qdrant embeds query and searches vectors
   ↓
9. Relevant documents returned to agent
   ↓
10. Agent synthesizes response with context
    ↓
11. Response returned to user with sources
```

### Document Addition Flow

```
1. User sends documents
   ↓
2. FastAPI receives POST /documents
   ↓
3. Documents validated (Pydantic)
   ↓
4. RAG Service forwards to Qdrant Service
   ↓
5. Qdrant Service embeds documents
   ↓
6. Vectors stored in Qdrant collection
   ↓
7. Document IDs returned to user
```

---

## Configuration Guide

### Environment Variables Priority

1. Environment variables (highest)
2. `.env` file
3. Default values (lowest)

### Configuration Validation

All settings are validated on startup using Pydantic:

```python
class Settings(BaseSettings):
    gemini_api_key: str = Field(...)  # Required
    gemini_model: str = Field(default="gemini/gemini-2.0-flash")
    # ... more fields
```

Missing required fields will raise an error on startup.

### Custom Configuration

To add new configuration:

1. Add field to `Settings` class in `src/config/settings.py`
2. Add to `.env.example` with documentation
3. Use via `settings.your_field_name`

Example:

```python
# In settings.py
class Settings(BaseSettings):
    my_custom_setting: str = Field(
        default="default_value",
        description="My custom setting"
    )

# In your code
from src.config import settings
value = settings.my_custom_setting
```

---

## Deployment Guide

### Local Development

```bash
# 1. Install dependencies
uv sync

# 2. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 3. Run the server
uv run python run.py
```

### Docker Deployment (Qdrant Only)

Start Qdrant in Docker:

```bash
docker-compose up -d
```

Configure app to use Docker Qdrant:

```env
QDRANT_MODE=remote
QDRANT_URL=http://localhost:6333
```

### Production Deployment

#### Option 1: Traditional Server

```bash
# 1. Install dependencies
uv sync

# 2. Set production environment
export ENVIRONMENT=production
export DEBUG=false

# 3. Run with Gunicorn/Uvicorn
uv run uvicorn src.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4 \
  --log-level info
```

#### Option 2: Docker Container

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy project files
COPY . .

# Install dependencies
RUN uv sync

# Expose port
EXPOSE 8000

# Run application
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t rag-chatbot-backend .
docker run -p 8000:8000 --env-file .env rag-chatbot-backend
```

#### Option 3: Cloud Platforms

**Heroku:**
```bash
# Procfile
web: uv run uvicorn src.main:app --host 0.0.0.0 --port $PORT
```

**Railway/Render:**
- Build command: `uv sync`
- Start command: `uv run uvicorn src.main:app --host 0.0.0.0 --port $PORT`

### Environment-Specific Configuration

**Development:**
```env
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG
QDRANT_MODE=local
```

**Production:**
```env
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
QDRANT_MODE=remote
QDRANT_URL=https://your-qdrant-cluster.cloud.qdrant.io
QDRANT_API_KEY=your_api_key
```

---

## API Reference

See interactive docs at http://localhost:8000/docs

### Authentication

Currently no authentication. To add:

1. Install `python-jose` and `passlib`
2. Add JWT token generation
3. Add `Depends(get_current_user)` to routes

### Rate Limiting

To add rate limiting:

```bash
uv add slowapi
```

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/chat")
@limiter.limit("5/minute")
async def chat(request: ChatRequest):
    ...
```

---

## Development Guide

### Project Setup

```bash
# Clone repository
git clone <repo-url>
cd backend

# Install dependencies
uv sync

# Run in development mode
uv run python run.py
```

### Adding New Endpoints

1. Create route in `src/routes/`
2. Define Pydantic models in `src/models/schemas.py`
3. Implement business logic in `src/services/`
4. Register router in `src/main.py`

Example:

```python
# src/routes/analytics.py
from fastapi import APIRouter

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/stats")
async def get_stats():
    return {"total_documents": 100}

# src/main.py
from .routes import analytics_router
app.include_router(analytics_router)
```

### Adding New Tools for Agent

```python
# In src/services/rag_service.py

@function_tool
def my_custom_tool(param: str) -> str:
    """Tool description for the agent."""
    # Implementation
    return result

# Add to agent
self.agent = Agent(
    name=settings.agent_name,
    tools=[search_knowledge_base, my_custom_tool]
)
```

### Testing

```bash
# Install test dependencies
uv add --dev pytest pytest-asyncio httpx

# Run tests
uv run pytest
```

Example test:

```python
# tests/test_chat.py
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_chat_endpoint():
    response = client.post(
        "/chat",
        json={"message": "Hello", "use_rag": False}
    )
    assert response.status_code == 200
    assert "response" in response.json()
```

### Logging

Logs are configured in `src/main.py`:

```python
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
```

To add logging in your module:

```python
import logging

logger = logging.getLogger(__name__)
logger.info("Message")
logger.error("Error", exc_info=True)
```

### Debugging

```python
# Add breakpoint
import pdb; pdb.set_trace()

# Or use VS Code debugger with launch.json:
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "src.main:app",
                "--reload"
            ],
            "jinja": true
        }
    ]
}
```

---

## Performance Optimization

### Caching

Add Redis caching:

```bash
uv add redis
```

```python
from redis import Redis
cache = Redis(host='localhost', port=6379)

@app.post("/chat")
async def chat(request: ChatRequest):
    cache_key = f"chat:{hash(request.message)}"
    cached = cache.get(cache_key)
    if cached:
        return cached
    # ... generate response
    cache.setex(cache_key, 3600, response)
```

### Database Connection Pooling

Qdrant client automatically manages connections.

### Async Operations

All I/O operations should be async:

```python
async def my_function():
    result = await some_async_operation()
    return result
```

---

## Security Considerations

1. **API Keys**: Never commit `.env` file
2. **CORS**: Configure `CORS_ORIGINS` properly
3. **Rate Limiting**: Add rate limits for production
4. **Input Validation**: All input validated by Pydantic
5. **Logging**: Don't log sensitive data

---

## Monitoring

### Health Checks

```bash
curl http://localhost:8000/health
```

### Metrics

To add Prometheus metrics:

```bash
uv add prometheus-client
```

### Error Tracking

To add Sentry:

```bash
uv add sentry-sdk
```

```python
import sentry_sdk
sentry_sdk.init(dsn="your-dsn")
```

---

## Troubleshooting

### Common Issues

1. **"Collection not found"**
   - Wait for initialization
   - Check `QDRANT_COLLECTION_NAME`

2. **"API key invalid"**
   - Verify `GEMINI_API_KEY`
   - Check quotas at Google AI Studio

3. **Memory issues**
   - Switch to `local-persistent` or `remote` mode
   - Reduce `VECTOR_SIZE` if possible

4. **Slow responses**
   - Reduce `MAX_SEARCH_RESULTS`
   - Use faster Gemini model
   - Enable caching

### Debug Mode

Enable detailed logging:

```env
DEBUG=true
LOG_LEVEL=DEBUG
```

---

## FAQ

**Q: Can I use OpenAI instead of Gemini?**
A: Yes, modify `rag_service.py` to use OpenAI model directly.

**Q: How do I scale this?**
A: Use remote Qdrant, add load balancer, run multiple workers.

**Q: Can I add authentication?**
A: Yes, use FastAPI's security utilities with OAuth2/JWT.

**Q: How do I backup data?**
A: For local-persistent mode, backup `qdrant_data/` directory. For remote, use Qdrant's backup features.

---

## Additional Resources

- [OpenAI Agents SDK Docs](https://openai.github.io/openai-agents-python/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LiteLLM Documentation](https://docs.litellm.ai/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
