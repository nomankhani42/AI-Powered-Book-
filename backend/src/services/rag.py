import os
from openai import OpenAI
from dotenv import load_dotenv
from qdrant_client import QdrantClient, models
from pydantic import BaseModel, Field
from agents import Agent, Runner, RunContextWrapper, FunctionTool # Added FunctionTool import

load_dotenv()

# Initialize OpenAI client for embeddings and chat completions via LiteLLM
# OPENAI_API_KEY will be your Gemini API Key
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("LITELLM_BASE_URL", "http://localhost:4000") # Assuming LiteLLM proxy runs on localhost:4000
)

# Initialize Qdrant Client
QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
QDRANT_GRPC_PORT = int(os.getenv("QDRANT_GRPC_PORT", 6334))
COLLECTION_NAME = "book_content"

if not QDRANT_HOST:
    raise ValueError("QDRANT_HOST environment variable not set. Please specify the Qdrant server address.")

qdrant_client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, grpc_port=QDRANT_GRPC_PORT)

# Initialize Embedding Model
EMBEDDING_MODEL = "gemini/text-embedding-001" # Using Gemini embedding model via LiteLLM
VECTOR_SIZE = 768 # Standard size for gemini/text-embedding-001

def get_embeddings(text: str):
    response = client.embeddings.create(
        input=text,
        model=EMBEDDING_MODEL
    )
    return response.data[0].embedding

# --- Qdrant Search Tool Definition ---
class QdrantSearchArgs(BaseModel):
    query: str = Field(..., description="The search query to find relevant book content.")

async def _qdrant_search_tool_invoke(ctx: RunContextWrapper, args: QdrantSearchArgs) -> str:
    """
    Searches the Qdrant collection for documents relevant to the query.
    """
    query_embedding = get_embeddings(args.query)

    search_result = qdrant_client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        limit=3  # Retrieve top 3 relevant documents
    )

    context = "\n".join([hit.payload["content"] for hit in search_result if hit.payload and "content" in hit.payload])
    return context if context else "No relevant information found."

qdrant_rag_tool = FunctionTool(
    name="qdrant_search",
    description="Searches the book content stored in Qdrant for relevant information to answer questions.",
    params_json_schema=QdrantSearchArgs.model_json_schema(),
    on_invoke_tool=_qdrant_search_tool_invoke,
)

# Initialize Agent
rag_agent = Agent(
    name="BookContentAssistant",
    instructions=(
        "You are an AI assistant for a book about Physical AI.\n"
        "Your goal is to answer questions based on the provided book content using the 'qdrant_search' tool.\n"
        "If the 'qdrant_search' tool does not return relevant information, state that you don't have enough information from the book to answer."
        "Always prioritize using the 'qdrant_search' tool to find relevant context before answering any question related to the book content or AI topics."
    ),
    tools=[qdrant_rag_tool],
    model="gemini-pro", # Use the appropriate Gemini model, assuming LiteLLM handles this.
)

# Placeholder for the refactored get_rag_response
# The actual implementation will be done in the next step.
async def get_rag_response(message: str) -> str:
    """
    Uses the rag_agent to get a response based on the user's message, leveraging Qdrant search.
    """
    try:
        # Create a Runner instance with the rag_agent
        result = await Runner.run(rag_agent, message)
        
        # Extract the final output from the agent's response
        if result.final_output:
            return result.final_output
        else:
            return "No specific response from the agent."
    except Exception as e:
        return f"Error getting RAG response from agent: {e}"

