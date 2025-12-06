# Quickstart: Update to `uv` and OpenAI Agents SDK

This guide provides instructions to set up and run the project locally after migrating to `uv`.

## Prerequisites

- Node.js (v18+)
- Python (v3.11+)
- uv

## Frontend Setup

(No changes to frontend setup)

1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Start the development server:
    ```bash
    npm start
    ```

The Docusaurus website should now be running at `http://localhost:3000`.

## Backend Setup

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```
2.  Create a virtual environment:
    ```bash
    uv venv
    ```
3.  Activate the virtual environment:
    ```bash
    source .venv/bin/activate
    ```
4.  Install dependencies with `uv`:
    ```bash
    uv pip install -r requirements.txt
    ```
5.  Create a `.env` file and add the necessary environment variables for Qdrant, Neon, and OpenAI.
6.  Start the development server:
    ```bash
    uvicorn src.api.main:app --reload
    ```

The FastAPI backend should now be running at `http://localhost:8000`.
