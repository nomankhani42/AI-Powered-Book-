# Quick Start Guide

Get your RAG Chatbot Backend up and running in 5 minutes!

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- Docker and Docker Compose ([Install](https://docs.docker.com/get-docker/))
- Gemini API key

## Step 1: Install uv (if not already installed)

```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Step 2: Get Your Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key

## Step 3: Setup Project

```bash
# Navigate to backend directory
cd backend

# Install dependencies (takes ~2 minutes)
uv sync

# Create .env file from example
cp .env.example .env
```

## Step 4: Start Qdrant Server

The backend uses Qdrant as a vector database. Start it with Docker:

```bash
# Start Qdrant server (from backend directory)
docker-compose up -d

# Verify it's running
curl http://localhost:6333/health
```

This runs Qdrant on `http://localhost:6333` with persistent storage.

**Alternative**: Use Qdrant Cloud instead - see [QDRANT_SETUP.md](QDRANT_SETUP.md)

## Step 5: Configure Environment

Open `.env` file and add your Gemini API key:

```env
# Required: Add your Gemini API key
GEMINI_API_KEY=your_api_key_here

# Qdrant server (Docker)
QDRANT_MODE=remote
QDRANT_URL=http://localhost:6333

# Optional: Model configuration
GEMINI_MODEL=gemini/gemini-2.0-flash
```

## Step 6: Start the Backend Server

```bash
uv run python run.py
```

You should see:

```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Step 7: Test the API

Open your browser and visit:

**Interactive API Docs:** http://localhost:8000/docs

Or test with curl:

```bash
# Health check
curl http://localhost:8000/health

# Add a document
curl -X POST http://localhost:8000/documents \
  -H "Content-Type: application/json" \
  -d '{
    "documents": [{
      "content": "Python is a programming language"
    }]
  }'

# Chat (without RAG)
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello! Tell me a joke.",
    "use_rag": false
  }'
```

## Step 8: Run Example Script

```bash
uv run python example_usage.py
```

This will:
1. Check API health
2. Add sample documents
3. Search the knowledge base
4. Chat with and without RAG
5. Show collection stats

## What's Next?

### Add Your Own Documents

```python
import requests

documents = {
    "documents": [
        {
            "content": "Your document content here",
            "metadata": {"source": "my_source"}
        }
    ]
}

response = requests.post(
    "http://localhost:8000/documents",
    json=documents
)
print(response.json())
```

### Chat with RAG

```python
import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={
        "message": "Your question here",
        "use_rag": True
    }
)

result = response.json()
print(f"Response: {result['response']}")
print(f"Sources: {result['sources']}")
```

### Enable Persistence

To keep your data between restarts, update `.env`:

```env
QDRANT_MODE=local-persistent
QDRANT_PATH=./qdrant_data
```

### Use Remote Qdrant

For production, use Qdrant Cloud or self-hosted:

```env
QDRANT_MODE=remote
QDRANT_URL=https://your-cluster.cloud.qdrant.io:6333
QDRANT_API_KEY=your_qdrant_api_key
```

## Common Issues

### "Failed to initialize Qdrant client"
- Check that `QDRANT_MODE` is set correctly
- Ensure no other process is using port 6333

### "API key not found"
- Make sure `.env` file exists in the backend directory
- Verify `GEMINI_API_KEY` is set correctly
- Don't include quotes around the API key value

### "Module not found"
- Make sure you're using `uv run` or activate the virtual environment:
  ```bash
  source .venv/bin/activate  # On Windows: .venv\Scripts\activate
  ```

### CORS errors from frontend
- Add your frontend URL to `CORS_ORIGINS` in `.env`:
  ```env
  CORS_ORIGINS=http://localhost:3000,http://localhost:5173
  ```

## Development Tips

### Hot Reload

The server automatically reloads when you make changes (thanks to `reload=True` in debug mode).

### View Logs

Set log level in `.env`:

```env
LOG_LEVEL=DEBUG  # Shows detailed logs
```

### Stop the Server

Press `Ctrl+C` in the terminal

### Reset Database

To clear all documents:

```bash
# Delete the data directory (for local-persistent mode)
rm -rf qdrant_data/

# Or use the API
curl -X DELETE http://localhost:8000/documents
```

## Architecture Overview

```
Your App/Frontend
       ↓
  FastAPI API
   ↓       ↓
RAG ←→ Qdrant
Service  (Vectors)
   ↓
 Gemini
  (LLM)
```

## File Structure

```
backend/
├── src/
│   ├── main.py          # FastAPI app
│   ├── config/          # Settings
│   ├── models/          # Request/response schemas
│   ├── routes/          # API endpoints
│   └── services/        # Business logic
├── .env                 # Your configuration
├── run.py              # Start script
└── example_usage.py    # Example code
```

## Next Steps

1. **Read the full docs**: See [README.md](README.md) for detailed information
2. **Explore the API**: Visit http://localhost:8000/docs
3. **Integrate with frontend**: Use the REST API from your app
4. **Deploy to production**: See [DOCS.md](DOCS.md) for deployment guide

## Need Help?

- Check [README.md](README.md) for full documentation
- Visit [DOCS.md](DOCS.md) for technical details
- Review [example_usage.py](example_usage.py) for code examples
- Open an issue in the repository

## Success! 🎉

Your RAG Chatbot Backend is now running!

Try it out:
- Visit http://localhost:8000/docs
- Run `uv run python example_usage.py`
- Build something amazing!
