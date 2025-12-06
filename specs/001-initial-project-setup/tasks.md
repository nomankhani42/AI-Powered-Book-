# Tasks: Initial Project Setup

**Input**: Design documents from `specs/001-initial-project-setup/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure.

- [X] T001 Create root project files
  - [X] T001.1 [P] Create `.gitignore`
  - [X] T001.2 [P] Create `README.md`
- [X] T002 Create `frontend` directory structure
  - [X] T002.1 [P] Initialize Docusaurus project in `frontend/`
  - [X] T002.2 [P] Create `frontend/src/components/Chatbot` directory
  - [X] T002.3 [P] Create `frontend/src/theme` directory
- [ ] T003 Create `backend` directory structure
  - [ ] T003.1 [P] Initialize Python project with Poetry in `backend/`
  - [ ] T003.2 [P] Create `backend/src/api` directory
  - [ ] T003.3 [P] Create `backend/src/core` directory
  - [ ] T003.4 [P] Create `backend/src/services` directory
  - [ ] T003.5 [P] Create `backend/src/models` directory
  - [ ] T003.6 [P] Create `backend/tests` directory
- [ ] T004 Create `docs` directory and initial content

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented.

- [ ] T005 [US1] Configure Docusaurus in `frontend/docusaurus.config.js`
- [ ] T006 [US1] Create Docusaurus navbar in `frontend/docusaurus.config.js`
- [ ] T007 [US1] Create Docusaurus footer in `frontend/docusaurus.config.js`
- [ ] T008 [US2] Setup FastAPI app in `backend/src/api/main.py`
- [ ] T009 [US2] Configure CORS middleware in `backend/src/api/main.py`
- [ ] T010 [US2] Setup database connection for Neon in `backend/src/core/db.py`
- [ ] T011 [US2] Setup Qdrant client in `backend/src/core/qdrant.py`

## Phase 3: User Story 1 - Read the Interactive Book (Priority: P1) 🎯 MVP

**Goal**: A user can navigate the interactive book website, read the content, and view the embedded media.
**Independent Test**: The Docusaurus site can be built and served locally, and the content is visible and correctly formatted.

- [ ] T012 [US1] Create `docs/intro.mdx`
- [ ] T013 [US1] Create `docs/chapter1.mdx`
- [ ] T014 [US1] Configure sidebars in `frontend/sidebars.js`

## Phase 4: User Story 2 - Interact with the RAG Chatbot (Priority: P2)

**Goal**: A user can ask the chatbot questions about the book's content.
**Independent Test**: The chatbot UI is visible, and it can respond to a hardcoded query.

### Implementation for User Story 2

- [ ] T015 [P] [US2] Create `ChatMessage` Pydantic model in `backend/src/models/chat.py`
- [ ] T016 [US2] Implement ingestion script in `backend/scripts/ingest.py`
- [ ] T017 [US2] Implement RAG service in `backend/src/services/rag.py`
- [ ] T018 [US2] Create chat endpoint in `backend/src/api/endpoints/chat.py`
- [ ] T019 [P] [US2] Create Chatbot React component in `frontend/src/components/Chatbot/index.js`
- [ ] T020 [P] [US2] Style Chatbot component in `frontend/src/components/Chatbot/styles.css`
- [ ] T021 [US2] Swizzle Docusaurus Root component to add Chatbot in `frontend/src/theme/Root.js`
- [ ] T022 [US2] Implement `highlight-to-ask` functionality in `frontend/src/theme/Root.js`

## Phase 5: Polish & Cross-Cutting Concerns

- [ ] T023 Setup CI/CD with GitHub Actions in `.github/workflows/deploy.yml`
- [ ] T024 Write Playwright E2E tests for user flows.
- [ ] T025 Write pytest unit tests for backend.
- [ ] T026 Write vitest unit tests for frontend.
- [ ] T027 Create deployment instructions for backend in `backend/DEPLOY.md`

## Dependencies & Execution Order

- **Phase 1 & 2**: Must be completed before any user story work.
- **User Story 1**: Can be completed independently after Phase 2.
- **User Story 2**: Depends on User Story 1 (for the chatbot to be embedded in the book).
- **Phase 5**: Can be worked on in parallel after user stories are complete.
