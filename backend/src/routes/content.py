"""
Content management routes for loading book content into the knowledge base.
"""

import logging
import re
from pathlib import Path
from fastapi import APIRouter, HTTPException, Query

from ..services import rag_service, qdrant_service


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/content", tags=["Content Management"])

# Path to book content (relative to backend directory)
DOCS_PATH = Path(__file__).parent.parent.parent.parent / "frontend" / "docs" / "book_modules"


def parse_markdown_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and content from markdown."""
    frontmatter = {}
    body = content

    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm_lines = parts[1].strip().split("\n")
            for line in fm_lines:
                if ":" in line:
                    key, value = line.split(":", 1)
                    frontmatter[key.strip()] = value.strip()
            body = parts[2].strip()

    return frontmatter, body


def chunk_content(content: str, chunk_size: int = 1000, overlap: int = 100) -> list[str]:
    """Split content into overlapping chunks for better RAG retrieval."""
    paragraphs = re.split(r'\n\n+', content)

    chunks = []
    current_chunk = ""

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        if len(current_chunk) + len(para) > chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            words = current_chunk.split()
            overlap_words = words[-overlap//5:] if len(words) > overlap//5 else []
            current_chunk = " ".join(overlap_words) + " " + para
        else:
            current_chunk += "\n\n" + para if current_chunk else para

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks


def load_markdown_files() -> list[dict]:
    """Load all markdown files from the docs directory."""
    documents = []

    if not DOCS_PATH.exists():
        logger.error(f"Docs path not found: {DOCS_PATH}")
        return documents

    for md_file in DOCS_PATH.rglob("*.md"):
        logger.info(f"Processing: {md_file.name}")

        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        frontmatter, body = parse_markdown_frontmatter(content)

        rel_path = md_file.relative_to(DOCS_PATH)
        parts = rel_path.parts
        module = parts[0] if len(parts) > 0 else "Unknown"
        chapter = md_file.stem

        chunks = chunk_content(body)

        for i, chunk in enumerate(chunks):
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


@router.post(
    "/load",
    summary="Load book content into knowledge base",
    description="Load all markdown files from the book into the Qdrant knowledge base. Use clear_existing=true to replace all content."
)
async def load_book_content(
    clear_existing: bool = Query(
        default=True,
        description="Clear existing documents before loading new content"
    ),
    force_recreate: bool = Query(
        default=False,
        description="Force recreate collection (use if you get vector dimension errors)"
    )
) -> dict:
    """
    Load book content from markdown files into the knowledge base.

    - **clear_existing**: If true, clears all existing documents first (recommended for updates)
    - **force_recreate**: If true, recreates the collection (fixes vector dimension mismatches)
    """
    try:
        logger.info(f"Loading book content (clear_existing={clear_existing}, force_recreate={force_recreate})")

        # Force recreate collection if requested (fixes vector dimension issues)
        if force_recreate:
            logger.info("Force recreating collection...")
            qdrant_service.recreate_collection()
        elif clear_existing:
            logger.info("Clearing existing documents...")
            qdrant_service.clear_collection()

        # Load markdown files
        documents = load_markdown_files()

        if not documents:
            raise HTTPException(
                status_code=404,
                detail=f"No markdown files found in {DOCS_PATH}"
            )

        logger.info(f"Found {len(documents)} document chunks")

        # Extract content and metadata
        contents = [doc["content"] for doc in documents]
        metadata = [doc["metadata"] for doc in documents]

        # Add to knowledge base
        try:
            doc_ids = rag_service.add_documents(contents, metadata)
        except Exception as e:
            # If we get a vector dimension error, suggest using force_recreate
            error_msg = str(e)
            if "incompatible" in error_msg.lower() or "vector" in error_msg.lower():
                raise HTTPException(
                    status_code=400,
                    detail=f"Vector dimension mismatch. Try again with force_recreate=true. Error: {error_msg}"
                )
            raise

        return {
            "success": True,
            "message": f"Successfully loaded {len(doc_ids)} document chunks",
            "stats": {
                "total_chunks": len(doc_ids),
                "cleared_existing": clear_existing,
                "force_recreated": force_recreate,
                "source_path": str(DOCS_PATH)
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error loading book content: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load book content: {str(e)}"
        )


@router.post(
    "/recreate-collection",
    summary="Recreate the Qdrant collection",
    description="Delete and recreate the collection with correct vector parameters. Use this to fix vector dimension mismatches."
)
async def recreate_collection() -> dict:
    """
    Recreate the Qdrant collection with correct vector parameters.
    WARNING: This will delete all existing documents!
    """
    try:
        logger.info("Recreating collection...")
        qdrant_service.recreate_collection()

        return {
            "success": True,
            "message": "Collection recreated successfully. You can now load content."
        }

    except Exception as e:
        logger.error(f"Error recreating collection: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to recreate collection: {str(e)}"
        )


@router.post(
    "/load-file",
    summary="Load a single markdown file",
    description="Load a specific markdown file by name into the knowledge base."
)
async def load_single_file(
    filename: str = Query(
        ...,
        description="Filename to load (e.g., 'Chapter_1_1_Introduction_to_Physical_AI.md')"
    )
) -> dict:
    """
    Load a single markdown file into the knowledge base.

    - **filename**: The markdown filename (e.g., 'Chapter_1_1_Introduction_to_Physical_AI.md')
    """
    try:
        logger.info(f"Loading single file: {filename}")

        # Find the file
        matching_files = list(DOCS_PATH.rglob(filename))

        if not matching_files:
            raise HTTPException(
                status_code=404,
                detail=f"File not found: {filename}. Available files: {[f.name for f in DOCS_PATH.rglob('*.md')]}"
            )

        md_file = matching_files[0]
        logger.info(f"Found file: {md_file}")

        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        frontmatter, body = parse_markdown_frontmatter(content)

        rel_path = md_file.relative_to(DOCS_PATH)
        parts = rel_path.parts
        module = parts[0] if len(parts) > 0 else "Unknown"
        chapter = md_file.stem

        chunks = chunk_content(body)

        documents = []
        for i, chunk in enumerate(chunks):
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

        if not documents:
            raise HTTPException(
                status_code=400,
                detail=f"No content chunks generated from {filename}"
            )

        contents = [doc["content"] for doc in documents]
        metadata = [doc["metadata"] for doc in documents]

        doc_ids = rag_service.add_documents(contents, metadata)

        return {
            "success": True,
            "message": f"Successfully loaded {len(doc_ids)} chunks from {filename}",
            "file": filename,
            "chunks": len(doc_ids)
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error loading file {filename}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load file: {str(e)}"
        )


@router.get(
    "/files",
    summary="List available markdown files",
    description="Get a list of all available markdown files that can be loaded."
)
async def list_files() -> dict:
    """List all available markdown files."""
    try:
        files = list(DOCS_PATH.rglob("*.md"))
        return {
            "files": [f.name for f in files],
            "count": len(files),
            "path": str(DOCS_PATH)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/status",
    summary="Get content status",
    description="Get information about the loaded book content."
)
async def get_content_status() -> dict:
    """Get status of the loaded book content."""
    try:
        # Get collection info
        collection_info = qdrant_service.get_collection_info()

        # Check if docs path exists
        docs_exist = DOCS_PATH.exists()
        md_files = list(DOCS_PATH.rglob("*.md")) if docs_exist else []

        return {
            "knowledge_base": {
                "collection_name": collection_info.get("name"),
                "document_count": collection_info.get("points_count", 0),
                "status": collection_info.get("status")
            },
            "source": {
                "path": str(DOCS_PATH),
                "exists": docs_exist,
                "markdown_files": len(md_files),
                "files": [f.name for f in md_files] if md_files else []
            }
        }

    except Exception as e:
        logger.error(f"Error getting content status: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get content status: {str(e)}"
        )
