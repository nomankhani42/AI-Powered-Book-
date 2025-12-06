"""
Example script demonstrating how to use the RAG Chatbot API.

Run this after starting the server: uv run python run.py
"""

import asyncio
import httpx


BASE_URL = "http://localhost:8000"


async def main():
    """Run example API calls."""
    async with httpx.AsyncClient() as client:
        print("=" * 60)
        print("RAG Chatbot API - Example Usage")
        print("=" * 60)

        # 1. Health Check
        print("\n1. Health Check")
        print("-" * 60)
        response = await client.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")

        # 2. Add Documents to Knowledge Base
        print("\n2. Adding Documents to Knowledge Base")
        print("-" * 60)
        documents = {
            "documents": [
                {
                    "content": "Python is a high-level, interpreted programming language known for its simplicity and readability. It was created by Guido van Rossum and first released in 1991.",
                    "metadata": {
                        "topic": "programming",
                        "language": "python"
                    }
                },
                {
                    "content": "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. It focuses on developing computer programs that can access data and learn from it.",
                    "metadata": {
                        "topic": "AI",
                        "category": "machine learning"
                    }
                },
                {
                    "content": "FastAPI is a modern, fast web framework for building APIs with Python. It's based on standard Python type hints and provides automatic API documentation, data validation, and high performance.",
                    "metadata": {
                        "topic": "web development",
                        "framework": "FastAPI"
                    }
                },
                {
                    "content": "Qdrant is a vector similarity search engine and vector database. It provides a production-ready service with a convenient API to store, search, and manage points with vectors and additional payloads.",
                    "metadata": {
                        "topic": "databases",
                        "type": "vector database"
                    }
                }
            ]
        }

        response = await client.post(f"{BASE_URL}/documents", json=documents)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Added {result['document_count']} documents")
        print(f"Document IDs: {result['document_ids'][:2]}...")

        # 3. Search Knowledge Base
        print("\n3. Searching Knowledge Base")
        print("-" * 60)
        search_query = {
            "query": "What is Python?",
            "limit": 3,
            "min_score": 0.3
        }

        response = await client.post(f"{BASE_URL}/documents/search", json=search_query)
        print(f"Status: {response.status_code}")
        results = response.json()
        print(f"Found {results['count']} results for: '{results['query']}'")
        for i, result in enumerate(results['results'][:2], 1):
            print(f"\n  Result {i}:")
            print(f"    Score: {result['score']:.3f}")
            print(f"    Content: {result['content'][:100]}...")

        # 4. Chat WITHOUT RAG (Direct LLM Response)
        print("\n4. Chat WITHOUT RAG (Direct LLM Response)")
        print("-" * 60)
        chat_request = {
            "message": "Tell me a short joke about programming",
            "use_rag": False
        }

        response = await client.post(f"{BASE_URL}/chat", json=chat_request)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {result['response']}")
        print(f"Used RAG: {result['metadata']['use_rag']}")

        # 5. Chat WITH RAG (Using Knowledge Base)
        print("\n5. Chat WITH RAG (Using Knowledge Base)")
        print("-" * 60)
        chat_request = {
            "message": "What is Python and what is it used for?",
            "use_rag": True,
            "session_id": "example_session_1"
        }

        response = await client.post(f"{BASE_URL}/chat", json=chat_request)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {result['response']}")
        print(f"\nUsed RAG: {result['metadata']['use_rag']}")
        if result['sources']:
            print(f"Number of sources: {len(result['sources'])}")
            print("\nTop Source:")
            source = result['sources'][0]
            print(f"  Score: {source['score']:.3f}")
            print(f"  Content: {source['content'][:100]}...")

        # 6. Another Chat with RAG
        print("\n6. Another Chat with RAG")
        print("-" * 60)
        chat_request = {
            "message": "What is machine learning?",
            "use_rag": True,
            "session_id": "example_session_1"
        }

        response = await client.post(f"{BASE_URL}/chat", json=chat_request)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {result['response']}")

        # 7. Get Collection Info
        print("\n7. Collection Information")
        print("-" * 60)
        response = await client.get(f"{BASE_URL}/documents/info")
        print(f"Status: {response.status_code}")
        info = response.json()
        print(f"Collection: {info['name']}")
        print(f"Points count: {info['points_count']}")
        print(f"Vectors count: {info['vectors_count']}")

        print("\n" + "=" * 60)
        print("Example completed successfully!")
        print("=" * 60)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except httpx.ConnectError:
        print("\n❌ Error: Could not connect to the API server.")
        print("Make sure the server is running:")
        print("  uv run python run.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")
