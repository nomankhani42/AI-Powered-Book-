# Qdrant Server Setup Guide

This guide shows you how to set up Qdrant as a remote server for your RAG chatbot.

## Option 1: Self-Hosted with Docker (Recommended for Development)

### Quick Start

The easiest way is to use the included `docker-compose.yml`:

```bash
# Start Qdrant server
docker-compose up -d

# Check if it's running
curl http://localhost:6333
```

**Your `.env` configuration:**
```env
QDRANT_MODE=remote
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=  # Leave empty for self-hosted
```

### What's Included

The `docker-compose.yml` file includes:
- **Qdrant Server** on port 6333 (REST API)
- **Qdrant Web UI** on port 6335 (optional dashboard)
- **Persistent storage** via Docker volumes

### Access Points

- **REST API**: http://localhost:6333
- **Web UI**: http://localhost:6335
- **Health Check**: http://localhost:6333/health

### Management Commands

```bash
# Start Qdrant
docker-compose up -d

# Stop Qdrant
docker-compose down

# View logs
docker-compose logs -f qdrant

# Restart Qdrant
docker-compose restart

# Stop and remove data (WARNING: deletes all data)
docker-compose down -v
```

### Verify Installation

```bash
# Check if Qdrant is running
curl http://localhost:6333/health

# Expected response:
# {"title":"qdrant - vector search engine","version":"1.x.x"}
```

---

## Option 2: Qdrant Cloud (Recommended for Production)

### Step 1: Create a Qdrant Cloud Account

1. Go to [https://cloud.qdrant.io/](https://cloud.qdrant.io/)
2. Sign up for a free account
3. Verify your email

### Step 2: Create a Cluster

1. Click **"Create Cluster"**
2. Choose your settings:
   - **Cluster Name**: e.g., `chatbot-rag`
   - **Cloud Provider**: AWS, GCP, or Azure
   - **Region**: Choose closest to your users
   - **Plan**: Start with Free tier (1GB)
3. Click **"Create"**

Wait 2-3 minutes for the cluster to be ready.

### Step 3: Get Your Credentials

1. Click on your cluster
2. Copy the **Cluster URL**
   - Example: `https://abc123-example.eu-central.aws.cloud.qdrant.io:6333`
3. Copy the **API Key**
   - Found under "API Keys" tab
   - Click "Create API Key" if needed

### Step 4: Configure Your Application

Update your `.env` file:

```env
QDRANT_MODE=remote
QDRANT_URL=https://your-cluster-id.region.aws.cloud.qdrant.io:6333
QDRANT_API_KEY=your_api_key_here
```

### Step 5: Test Connection

```bash
# Start your application
uv run python run.py

# Check health endpoint
curl http://localhost:8000/health

# Should show:
# {
#   "status": "healthy",
#   "qdrant_connected": true,
#   "collection_exists": true
# }
```

---

## Option 3: Manual Docker Installation

If you don't want to use docker-compose:

```bash
# Pull Qdrant image
docker pull qdrant/qdrant

# Run Qdrant with persistent storage
docker run -p 6333:6333 -p 6334:6334 \
  -v $(pwd)/qdrant_storage:/qdrant/storage:z \
  qdrant/qdrant
```

---

## Troubleshooting

### Connection Refused

**Problem**: `Connection refused` when trying to connect to Qdrant

**Solutions**:
```bash
# Check if Docker is running
docker ps

# Check if Qdrant container is running
docker-compose ps

# Restart Qdrant
docker-compose restart qdrant

# Check Qdrant logs
docker-compose logs qdrant
```

### Port Already in Use

**Problem**: Port 6333 is already in use

**Solution**: Change the port in `docker-compose.yml`:
```yaml
ports:
  - "6334:6333"  # Use port 6334 instead
```

Then update `.env`:
```env
QDRANT_URL=http://localhost:6334
```

### "Collection not found"

**Problem**: Application says collection doesn't exist

**Solution**: The application creates the collection automatically on first run. Just add some documents:

```bash
curl -X POST http://localhost:8000/documents \
  -H "Content-Type: application/json" \
  -d '{
    "documents": [{
      "content": "Test document"
    }]
  }'
```

### Qdrant Cloud Connection Issues

**Problem**: Can't connect to Qdrant Cloud

**Checklist**:
- ✅ Cluster status is "Running" (not "Starting")
- ✅ Copied full URL including `https://` and port `:6333`
- ✅ API key is correct (no extra spaces)
- ✅ Your IP is not blocked by firewall

**Test connection directly**:
```bash
curl -H "api-key: your_api_key" \
  https://your-cluster.cloud.qdrant.io:6333/health
```

---

## Monitoring & Management

### Web UI (Docker only)

Visit http://localhost:6335 to:
- Browse collections
- View points/vectors
- Run test queries
- Monitor performance

### REST API

```bash
# List all collections
curl http://localhost:6333/collections

# Get collection info
curl http://localhost:6333/collections/chatbot_documents

# Count points
curl http://localhost:6333/collections/chatbot_documents/points/count
```

### Python Client (Direct)

```python
from qdrant_client import QdrantClient

client = QdrantClient(
    url="http://localhost:6333",
    # api_key="your_key"  # Only for Qdrant Cloud
)

# List collections
print(client.get_collections())

# Get collection info
info = client.get_collection("chatbot_documents")
print(f"Points: {info.points_count}")
```

---

## Performance Tips

### Docker Resource Allocation

For better performance, allocate more resources to Docker:

**Docker Desktop Settings:**
- CPU: 2+ cores
- Memory: 4GB+ RAM
- Swap: 1GB

### Qdrant Cloud Scaling

Monitor your usage in the Qdrant Cloud dashboard:
- Upgrade to higher tier if you need more storage
- Consider multi-node clusters for production
- Enable backups for critical data

---

## Data Backup

### Docker (Self-Hosted)

```bash
# Backup data directory
tar -czf qdrant_backup_$(date +%Y%m%d).tar.gz qdrant_storage/

# Restore from backup
tar -xzf qdrant_backup_YYYYMMDD.tar.gz
```

### Qdrant Cloud

Qdrant Cloud includes automatic backups:
- Daily snapshots (retained for 7 days)
- Manual snapshots available
- Point-in-time recovery

Access backups from your cluster dashboard.

---

## Migration

### From Local to Remote

1. **Export data** (if you have local data):
```python
from qdrant_client import QdrantClient

local_client = QdrantClient(path="./qdrant_data")
remote_client = QdrantClient(url="http://localhost:6333")

# Get all points
points = local_client.scroll(
    collection_name="chatbot_documents",
    limit=10000
)[0]

# Upload to remote
remote_client.upsert(
    collection_name="chatbot_documents",
    points=points
)
```

2. **Update `.env`**:
```env
QDRANT_MODE=remote
QDRANT_URL=http://localhost:6333
```

3. **Restart application**

---

## Security Best Practices

### Self-Hosted

- Don't expose Qdrant port publicly (use behind firewall/VPN)
- Use reverse proxy (nginx) with SSL
- Enable authentication if needed
- Keep Docker images updated

### Qdrant Cloud

- Rotate API keys regularly
- Use different keys for dev/staging/prod
- Enable IP whitelisting if available
- Monitor access logs

---

## Next Steps

Once Qdrant is running:

1. ✅ Start your FastAPI backend: `uv run python run.py`
2. ✅ Check health: `curl http://localhost:8000/health`
3. ✅ Add documents: Use the `/documents` endpoint
4. ✅ Test RAG: Use the `/chat` endpoint

See the main [README.md](README.md) for API usage examples.

---

## Support

- **Qdrant Documentation**: https://qdrant.tech/documentation/
- **Qdrant Cloud Support**: https://cloud.qdrant.io/
- **Qdrant Discord**: https://discord.gg/qdrant
- **GitHub Issues**: https://github.com/qdrant/qdrant/issues
