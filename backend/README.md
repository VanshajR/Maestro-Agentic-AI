# Agentic AI Automator Backend

FastAPI backend for orchestrating the Agentic AI Automator system with Groq + Hugging Face LLM fallbacks, modular tools, and structured observability.

## Features

- Async FastAPI with `/api/v1/agent/plan`, `/api/v1/agent/execute`, and `/api/v1/health`
- Planner + executor pipeline using Groq models with automatic rate-limit failover and Hugging Face fallback
- Tool registry with web fetcher, GitHub search, PDF extractor, web search, and summarization
- Structured JSON logging, rate limiting, optional API key auth middleware, and centralized error handlers
- Retry logic for all external services

## Environment Variables

| Variable | Description |
| --- | --- |
| `GROQ_API_KEY` | Required for Groq completion endpoint |
| `GROQ_MODELS` | Optional comma-separated model list; defaults match production catalog |
| `HF_API_KEY` | Optional Hugging Face Inference token |
| `GITHUB_TOKEN` | Optional token for GitHub search rate limits |
| `SERP_API_KEY` | Optional SerpAPI key for search |
| `API_AUTH_KEY` | Optional shared secret for `x-api-key` header |
| `RATE_LIMIT_PER_MINUTE` | Requests per minute per IP (default 60) |
| `CORS_ORIGINS` | JSON array of allowed origins |

Create a `.env` file or pass these as deployment secrets.

## Local Development

```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: . .venv/Scripts/Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API docs are available under `http://localhost:8000/docs`.

## Testing the Agent Endpoints

```bash
curl -X POST http://localhost:8000/api/v1/agent/execute \
  -H "Content-Type: application/json" \
  -d '{"plan_request":{"goal":"Summarize the newest Groq models","max_steps":4}}'
```

The response includes the generated plan, intermediate tool outputs, and a merged summary.

## Docker

```bash
docker build -t agentic-backend .
docker run -it --rm -p 8000:8000 --env-file .env agentic-backend
```
