# Tasks: Backend Rewrite for Chatbot with FastAPI, OpenAI Agents, and Qdrant

**Input**: Design documents from `specs/004-backend-chatbot-rewrite/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

## Phase 1: Setup and Core FastAPI Application

**Purpose**: Initialize the FastAPI project and establish foundational elements.

-   [ ] T001 [P] Create `backend/src/main.py` with a basic FastAPI application instance.
-   [ ] T002 [P] Configure `backend/requirements.txt` with initial dependencies: `fastapi`, `uvicorn`, `openai`, `qdrant-client`, `pydantic`.
-   [ ] T003 [P] Create `backend/src/core/config.py` for environment variable management (e.g., OpenAI API key, Qdrant URL).
-   [ ] T004 Implement a basic `/health` GET endpoint in `backend/src/api/health.py` and integrate it into `main.py`.
-   [ ] T005 Write unit tests for `backend/src/core/config.py` to ensure settings are loaded correctly.
-   [ ] T006 [P] Create `backend/tests/test_main.py` and add a test for the `/health` endpoint.

## Phase 2: Qdrant Integration and Content Ingestion

**Purpose**: Set up Qdrant service and implement the content ingestion API.

-   [ ] T007 [P] Create `backend/src/services/qdrant_service.py` with a class to manage Qdrant connection and collection operations (create, upsert, search).
-   [ ] T008 [P] Define Pydantic models for content ingestion requests and responses in `backend/src/models/ingest.py`.
-   [ ] T009 Implement a content chunking utility function in `backend/src/services/utils.py` (or similar) to break down large texts.
-   [ ] T010 Implement content vectorization using OpenAI embeddings in `backend/src/services/openai_service.py`.
-   [ ] T011 Create the `backend/src/api/ingest.py` module with the `/ingest_content` POST endpoint, integrating `qdrant_service` and `openai_service` for processing.
-   [ ] T012 Write unit tests for `backend/src/services/qdrant_service.py` (mocking external calls).
-   [ ] T013 Write unit tests for the content chunking utility.
-   [ ] T014 Write integration tests for the `/ingest_content` endpoint in `backend/tests/test_api.py`.

## Phase 3: OpenAI Agents and RAG Integration

**Purpose**: Implement the RAG pipeline and the main chatbot API endpoint.

-   [ ] T015 Enhance `backend/src/services/openai_service.py` to include chat completion functionality with conversational context.
-   [ ] T016 Create `backend/src/services/rag_service.py` to orchestrate the RAG pipeline:
    -   Takes user query and conversational history.
    -   Uses `openai_service` for embedding the query.
    -   Uses `qdrant_service` to search for relevant book content.
    -   Constructs a prompt for the OpenAI model, including retrieved context and conversation history.
    -   Uses `openai_service` for final response generation.
-   [ ] T017 Define Pydantic models for chat requests and responses in `backend/src/models/chat.py`.
-   [ ] T018 Create the `backend/src/api/chat.py` module with the `/chat` POST endpoint, integrating `rag_service` for conversational responses.
-   [ ] T019 Implement session management logic (basic in-memory or a simple store) for conversational context.
-   [ ] T020 Write unit tests for `backend/src/services/rag_service.py` (mocking OpenAI and Qdrant).
-   [ ] T021 Write integration tests for the `/chat` endpoint in `backend/tests/test_api.py`.

## Phase 4: Polish, Documentation, and Refinements

**Purpose**: Finalize the implementation, ensure quality, and prepare for deployment.

-   [ ] T022 Update API documentation (e.g., using FastAPI's built-in OpenAPI/Swagger UI capabilities).
-   [ ] T023 Review and refine error handling across all API endpoints and services.
-   [ ] T024 Ensure all sensitive information (API keys) is loaded from environment variables via `core/config.py`.
-   [ ] T025 Add comments and type hints for improved code readability and maintainability.
-   [ ] T026 Update `start_server.ps1` to correctly launch the new FastAPI application.
-   [ ] T027 Manually test content ingestion and chatbot interaction.

## Dependencies & Execution Order

-   **Phase 1**: Must be completed first.
-   **Phase 2**: Depends on Phase 1 completion. T007, T008, T009, T010 can be developed in parallel, but T011 depends on them.
-   **Phase 3**: Depends on Phase 2 completion. T015, T016, T017 can be developed in parallel, but T018 depends on them.
-   **Phase 4**: Depends on Phase 3 completion.

## Implementation Strategy

### Incremental Delivery

1.  Complete Phase 1: Setup and Core FastAPI Application
2.  Complete Phase 2: Qdrant Integration and Content Ingestion
3.  Complete Phase 3: OpenAI Agents and RAG Integration
4.  Complete Phase 4: Polish, Documentation, and Refinements
