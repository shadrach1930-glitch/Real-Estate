# Backend — FastAPI

Python + FastAPI backend for the PrimeHomes Realty Lead Bot.

## Current Capabilities

- Full database models + Alembic
- REST API (chat, leads, conversations, follow-ups, dashboard)
- Deterministic lead scoring
- n8n webhook integration
- **AI Lead Extraction** (Phase 6)
  - Configurable provider/model
  - Structured JSON schema validation
  - Nigerian currency & property normalization
  - Rule-based fallback when no AI key is set

## AI Configuration

In `.env`:

```env
AI_PROVIDER=openai          # or google, etc.
AI_MODEL=gpt-4o-mini
AI_API_KEY=sk-...
AI_TEMPERATURE=0.2
AI_MAX_TOKENS=1000
```

When `AI_API_KEY` is empty the system uses a deterministic rule-based extractor so local development works without an API key.

## Local Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Postgres
docker compose up -d postgres

alembic revision --autogenerate -m "initial schema"
alembic upgrade head

uvicorn app.main:app --reload --port 8000
```

- Health: http://localhost:8000/health
- Docs:   http://localhost:8000/docs
