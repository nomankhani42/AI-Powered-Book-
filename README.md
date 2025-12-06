# AI Powered Book

This project is an interactive, open-source, university-grade textbook on Physical AI & Humanoid Robotics. It features an embedded AI teaching assistant capable of answering questions about the book's content.

## Features

- **Interactive Book**: The book is built with Docusaurus and MDX, providing an interactive and engaging reading experience.
- **RAG Chatbot**: An embedded chatbot, powered by a Retrieval-Augmented Generation (RAG) pipeline, can answer questions about the book's content.
- **Highlight-to-Ask**: Users can highlight text and ask the chatbot questions about the selection.

## Tech Stack

- **Frontend**: Docusaurus 3.x, React 19, MDX 3, TailwindCSS 3.x
- **Backend**: FastAPI, LiteLLM (with Gemini 2.0 Flash/Pro)
- **Database**: Qdrant (Vector DB), Neon (Postgres for metadata)
- **Testing**: Playwright (E2E), pytest (backend), Vitest (frontend)
- **Deployment**: GitHub Actions, GitHub Pages, Railway/Fly.io/Render

## Getting Started

See the [Quickstart guide](specs/001-initial-project-setup/quickstart.md) for instructions on how to set up and run the project locally.
