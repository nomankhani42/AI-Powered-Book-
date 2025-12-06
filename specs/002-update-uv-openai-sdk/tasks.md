# Tasks: Update to `uv` and OpenAI Agents SDK

**Input**: Design documents from `specs/002-update-uv-openai-sdk/`
**Prerequisites**: plan.md, spec.md, research.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare the environment for the changes.

- [X] T001 [P] Ensure `uv` is installed globally.
- [X] T002 [P] Create `backend/requirements.txt` from `backend/pyproject.toml`
  `poetry export -f requirements.txt --output backend/requirements.txt --without-hashes`
- [X] T003 Remove `poetry.lock` in `backend/poetry.lock`

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure changes for dependency management and AI framework.

### User Story 1 - Developer initializes the project (Priority: P1)

**Goal**: A developer can initialize the Python backend project and install dependencies using the `uv` command-line tool.
**Independent Test**: A developer can successfully run `uv pip install -r requirements.txt` (or equivalent `uv` command) in the `backend` directory.

- [X] T004 [US1] Remove `[tool.poetry]` section from `backend/pyproject.toml`
- [X] T005 [US1] Update `quickstart.md` in `specs/002-update-uv-openai-sdk/quickstart.md` to reflect `uv` usage.

### User Story 2 - Chatbot uses OpenAI Agents SDK (Priority: P1)

**Goal**: The RAG chatbot uses the OpenAI Agents SDK for its AI framework, replacing the previous LiteLLM implementation.
**Independent Test**: The chatbot can respond to a query, and the backend logs show that the OpenAI Agents SDK was used.

- [X] T006 [US2] Install `openai` library using `uv` in `backend/`
- [X] T007 [US2] Update `backend/.env` (or equivalent) to include `OPENAI_API_KEY`.
- [X] T008 [US2] Refactor `backend/src/services/rag.py` to use OpenAI Agents SDK.
- [X] T009 [US2] Remove `LiteLLM` related code from `backend/src/services/rag.py`.

## Phase 3: Polish & Cross-Cutting Concerns

- [X] T010 [P] Update `GEMINI.md` to remove `LiteLLM` and add `uv` and `openai` as core technologies. (This was done by `update-agent-context.ps1` but might need manual review).
- [X] T011 Verify `quickstart.md` (in `specs/001-initial-project-setup/`) is replaced with the new `quickstart.md` (from `specs/002-update-uv-openai-sdk/`).

## Dependencies & Execution Order

- **Phase 1**: Must be completed first.
- **Phase 2**: User Story 1 and User Story 2 can be worked on in parallel within this phase, but both depend on Phase 1 completion.
- **Phase 3**: Depends on Phase 2 completion.

## Implementation Strategy

### Incremental Delivery

1. Complete Phase 1.
2. Complete User Story 1 tasks.
3. Complete User Story 2 tasks.
4. Complete Phase 3 tasks.
