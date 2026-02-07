# SQL LLM Agent

A FastAPI-based LLM agent designed for SQL interaction, featuring RAG support and MCP (Model Context Protocol) integration.

## Features

- **Unified Chat Endpoint**: Interact with the agent via a single endpoint.
- **SQL Generation & Validation**: Natural language to SQL conversion with safe execution and validation.
- **RAG Support**: Retrieval-Augmented Generation for schema and documentation.
- **MCP Integration**: Implements the Model Context Protocol for tool use.
- **Modular Architecture**: Clean separation of concerns (Agents, LLM, DB, RAG).

## Setup

1.  Clone the repository.
2.  Copy `.env.example` to `.env` and configure your environment variables.
3.  Install dependencies: `poetry install`
4.  Run the application: `uvicorn app.main:app --reload`

## Docker

Run with Docker Compose:

```bash
docker-compose up --build
```
