# Tasks: Book Content Structure and Learning Path

**Input**: Design documents from `specs/003-book-content-structure/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare the Docusaurus environment for content structuring.

- [X] T001 [P] Ensure Docusaurus project is initialized in `frontend/`. (Already done in `001-initial-project-setup`)
- [X] T002 [P] Create `docs/modules` directory for module organization.

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Implement the core content organization (modules, chapters).

### User Story 1 - Content Creator defines book structure (Priority: P1)

**Goal**: A content creator can define the book's structure into modules and chapters, and associate these with a weekly learning path.
**Independent Test**: The book structure (modules, chapters, learning path) can be clearly defined in configuration files and reflected in the website navigation.

- [X] T003 [US1] Create `docs/modules/module1` directory for the first module.
- [X] T004 [US1] Create `docs/modules/module1/chapter1.mdx` with basic content and `week: 1` in front matter.
- [X] T005 [US1] Create `docs/modules/module1/chapter2.mdx` with basic content and `week: 1` in front matter.
- [X] T006 [US1] Create `docs/modules/module2` directory for the second module.
- [X] T007 [US1] Create `docs/modules/module2/chapter3.mdx` with basic content and `week: 2` in front matter.
- [X] T008 [US1] Create `docs/modules/module2/chapter4.mdx` with basic content and `week: 2` in front matter.
- [X] T009 [US1] Create `docs/modules/module3` directory for the third module.
- [X] T010 [US1] Create `docs/modules/module3/chapter5.mdx` with basic content and `week: 3` in front matter.
- [X] T011 [US1] Create `docs/modules/module3/chapter6.mdx` with basic content and `week: 3` in front matter.
- [ ] T012 [US1] Configure `frontend/sidebars.js` to autogenerate sidebar from `docs/modules`.

## Phase 3: User Story 2 - Reader navigates learning path (Priority: P1)

**Goal**: A reader can navigate the book content following a defined weekly learning path.
**Independent Test**: A reader can see the weekly learning path and use it to access relevant chapters.

- [ ] T013 [US2] Research Docusaurus client-side APIs to access docs metadata.
- [ ] T014 [US2] Create custom React component `frontend/src/theme/LearningPath.js` to display weekly learning path.
- [ ] T015 [US2] Integrate `LearningPath.js` component into Docusaurus (e.g., as a custom page or sidebar item).
- [ ] T016 [US2] Style `LearningPath.js` component using TailwindCSS.

## Phase 4: Polish & Cross-Cutting Concerns

- [ ] T017 Update `frontend/docusaurus.config.js` with any necessary plugin configurations.
- [ ] T018 Ensure navigation is consistent between module/chapter structure and learning path.
- [ ] T019 Write E2E tests with Playwright for learning path navigation.
- [ ] T020 Manually review the implemented structure and learning path for usability.

## Dependencies & Execution Order

- **Phase 1**: Must be completed first.
- **Phase 2**: Depends on Phase 1 completion. Tasks T003-T006 can be done sequentially.
- **Phase 3**: Depends on Phase 2 completion. Tasks T007-T010 can be done sequentially.
- **Phase 4**: Depends on Phase 3 completion.

## Implementation Strategy

### Incremental Delivery

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (User Story 1 tasks)
3. Complete Phase 3: User Story 2 tasks
4. Complete Phase 4: Polish & Cross-Cutting Concerns
