---
id: 1
title: Amend Constitution for Physical AI Book
stage: constitution
date: 2025-12-02
surface: agent
model: gemini-1.5-pro
feature: none
branch: main
user: unspecified
command: /sp.constitution
labels: [constitution, project-scoping]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

/sp.constitution # PROJECT CONSTITUTION  
**Physical AI & Humanoid Robotics – The Complete Interactive Book + Embedded RAG Chatbot**

## Vision & Purpose
Create the world’s first fully interactive, open-source, university-grade textbook on Physical AI & Humanoid Robotics that lives on the public internet with a built-in AI teaching assistant capable of answering any question — globally or from selected text only.

## Success Criteria (Measurable)
- Book deployed and live on GitHub Pages (100% free forever)
- Embedded RAG chatbot works on every page
- Chatbot supports two modes:
  1. Global Q&A about the entire book
  2. “Ask about this selection only” (user highlights text → instant contextual answer)
- Zero hallucinated or outdated code/documentation (enforced via Context7 MCP)
- All code passes Context7 verification for 2025 versions of every library
- Full source MIT-licensed, reproducible in <10 minutes

## Scope
### In Scope
- Docusaurus 3.x + Spec-Kit Plus book
- All course content converted to beautiful MDX
- FastAPI + OpenAI Agents SDK (or LiteLLM + Gemini) RAG backend
- Qdrant Cloud (free tier) + Neon Serverless Postgres
- Text-selection-aware chatbot (highlight → right-click → Ask)
- Full ingestion pipeline
- GitHub Actions CI/CD to GitHub Pages
- Railway / Fly.io / Render free-tier backend deploy

### Out of Scope
- Paid cloud GPUs
- Authentication (anonymous public access only)
- Mobile app (web-first, PWA ready)

## Tech Stack (December 2025 – Context7 Enforced)
- Docusaurus 3.x (latest)
- React 19 + MDX 3
- TailwindCSS 3.x
- FastAPI (latest 2025)
- OpenAI Agents SDK or LiteLLM (Gemini 2.0 Flash/Pro)
- Qdrant Cloud REST + Python client (latest)
- Neon Serverless Postgres (pgvector optional)
- Context7 MCP server (mandatory for every code task)
- GitHub Actions + GitHub Pages

## Architecture Overview
```mermaid
flowchart TD
    A[User Browser] --> B[Docusaurus GitHub Pages]
    B --> C[React Chatbot Component]
    C --> D[FastAPI Backend (Railway/Fly.io)]
    D --> E[Qdrant Cloud Vector DB]
    D --> F[Neon Postgres (metadata)]
    E & F --> G[Gemini 2.0 / OpenAI via LiteLLM]
    H[Context7 MCP] -->|.use context7| I[Every Code Generation Step]
```

## Response snapshot

I have updated the project constitution to version 1.0.0. This was a major update, replacing the placeholder template with the detailed project vision, scope, and architecture you provided.

I have also created a Prompt History Record (PHR) for this action: `history/prompts/constitution/1-amend-constitution-for-physical-ai-book.constitution.prompt.md`.

Suggested commit message:
`docs: amend constitution to v1.0.0 (project initialization)`

## Outcome

- ✅ Impact: Major. The project constitution was completely rewritten, establishing the foundational principles for the project.
- 🧪 Tests: None. This was a documentation change.
- 📁 Files: 1 file modified: `.specify/memory/constitution.md`.
- 🔁 Next prompts: The user may want to proceed with creating a spec, plan, or tasks based on the new constitution.
- 🧠 Reflection: The user provided a very detailed constitution, which made the update straightforward. The process of checking the other templates for consistency is a good practice to ensure the project's documentation stays in sync.

## Evaluation notes (flywheel)

- Failure modes observed: The `create-phr.sh` script was not found, requiring a fallback to the agent-native PHR creation flow. This indicates a potential mismatch between the documented and actual project scripts.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
