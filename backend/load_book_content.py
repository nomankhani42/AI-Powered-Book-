"""
Script to load book content from frontend docs into Qdrant knowledge base.
Run this script after starting the backend to populate the RAG knowledge base.
"""

import os
import re
import httpx
import asyncio
from pathlib import Path

# Backend API URL
API_URL = "http://localhost:8000"

# Path to book content
DOCS_PATH = Path(__file__).parent.parent / "frontend" / "docs" / "book_modules"


def parse_markdown_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and content from markdown."""
    frontmatter = {}
    body = content

    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            # Parse simple frontmatter
            fm_lines = parts[1].strip().split("\n")
            for line in fm_lines:
                if ":" in line:
                    key, value = line.split(":", 1)
                    frontmatter[key.strip()] = value.strip()
            body = parts[2].strip()

    return frontmatter, body


def chunk_content(content: str, chunk_size: int = 1000, overlap: int = 100) -> list[str]:
    """Split content into overlapping chunks for better RAG retrieval."""
    # Split by paragraphs first
    paragraphs = re.split(r'\n\n+', content)

    chunks = []
    current_chunk = ""

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        # If adding this paragraph exceeds chunk size, save current and start new
        if len(current_chunk) + len(para) > chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            # Keep some overlap from the end of previous chunk
            words = current_chunk.split()
            overlap_words = words[-overlap//5:] if len(words) > overlap//5 else []
            current_chunk = " ".join(overlap_words) + " " + para
        else:
            current_chunk += "\n\n" + para if current_chunk else para

    # Don't forget the last chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks


def load_markdown_files() -> list[dict]:
    """Load all markdown files from the docs directory."""
    documents = []

    if not DOCS_PATH.exists():
        print(f"Docs path not found: {DOCS_PATH}")
        return documents

    # Find all markdown files
    for md_file in DOCS_PATH.rglob("*.md"):
        print(f"Processing: {md_file.name}")

        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Parse frontmatter and content
        frontmatter, body = parse_markdown_frontmatter(content)

        # Extract chapter/module info from path
        rel_path = md_file.relative_to(DOCS_PATH)
        parts = rel_path.parts
        module = parts[0] if len(parts) > 0 else "Unknown"
        chapter = md_file.stem

        # Chunk the content
        chunks = chunk_content(body)

        for i, chunk in enumerate(chunks):
            # Skip very small chunks
            if len(chunk) < 50:
                continue

            documents.append({
                "content": chunk,
                "metadata": {
                    "source": str(rel_path),
                    "module": module,
                    "chapter": chapter,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    **frontmatter
                }
            })

    return documents


async def upload_documents(documents: list[dict]) -> bool:
    """Upload documents to the backend API."""
    if not documents:
        print("No documents to upload")
        return False

    print(f"\nUploading {len(documents)} document chunks to knowledge base...")

    # Format for API
    api_documents = [
        {
            "content": doc["content"],
            "metadata": doc["metadata"]
        }
        for doc in documents
    ]

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            # First check if backend is healthy
            health_resp = await client.get(f"{API_URL}/health")
            if health_resp.status_code != 200:
                print(f"Backend health check failed: {health_resp.text}")
                return False

            print("Backend is healthy, uploading documents...")

            # Upload documents
            response = await client.post(
                f"{API_URL}/documents/",
                json={"documents": api_documents}
            )

            if response.status_code == 200:
                result = response.json()
                print(f"Successfully uploaded {result['document_count']} documents!")
                return True
            else:
                print(f"Upload failed: {response.status_code} - {response.text}")
                return False

        except httpx.ConnectError:
            print(f"Could not connect to backend at {API_URL}")
            print("Make sure the backend is running: cd backend && uv run python main.py")
            return False
        except Exception as e:
            print(f"Error uploading documents: {e}")
            return False


async def main():
    """Main function to load book content."""
    print("=" * 60)
    print("Book Content Loader for RAG Knowledge Base")
    print("=" * 60)

    # Load markdown files
    print("\nLoading markdown files from:", DOCS_PATH)
    documents = load_markdown_files()

    if not documents:
        print("No documents found!")
        return

    print(f"\nFound {len(documents)} document chunks from book content")

    # Show sample
    print("\nSample document:")
    print(f"  - Content preview: {documents[0]['content'][:100]}...")
    print(f"  - Metadata: {documents[0]['metadata']}")

    # Upload to backend
    success = await upload_documents(documents)

    if success:
        print("\n" + "=" * 60)
        print("Book content loaded successfully!")
        print("The chatbot now has access to the book knowledge base.")
        print("=" * 60)
    else:
        print("\nFailed to load book content. Check the errors above.")


if __name__ == "__main__":
    asyncio.run(main())
