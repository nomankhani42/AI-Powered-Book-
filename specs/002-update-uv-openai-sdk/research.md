# Research: Update to `uv` and OpenAI Agents SDK

This document outlines the research and decisions made for updating the backend tooling.

## Technology Choices

| Technology | Decision | Rationale | Alternatives Considered |
|---|---|---|---|
| Dependency Manager | `uv` | The user requested to use `uv` for project initialization. `uv` is a fast, modern Python package installer and resolver. | `poetry`, `pip` |
| AI Framework | OpenAI Agents SDK | The user requested to use the OpenAI Agents SDK. | `LiteLLM` |

## Migration from `poetry` to `uv`

1.  **Remove `poetry.lock`**: This file is specific to `poetry` and is not needed by `uv`.
2.  **Generate `requirements.txt`**: `uv` works with `requirements.txt` files. We can generate this from the `pyproject.toml` file.
    ```bash
    poetry export -f requirements.txt --output requirements.txt --without-hashes
    ```
3.  **Update `pyproject.toml`**: The `[tool.poetry]` section can be removed. `uv` does not require it.
4.  **Update `quickstart.md`**: The instructions for setting up the backend need to be updated to use `uv`.

## Using the OpenAI Agents SDK

The `openai` agents SDK provides a framework for building AI agents. The existing RAG service in `backend/src/services/rag.py` will be updated to use this SDK. This will involve:

1.  Installing the `openai` library.
2.  Updating the environment variables to include the `OPENAI_API_KEY`.
3.  Refactoring the `rag.py` service to use the `openai` client and its agent creation and execution methods.

## Context7 Commands

- **uv**: `use context7 /astral-sh/uv`
- **openai**: `use context7 /openai/openai-python`
