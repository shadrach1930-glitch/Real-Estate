# Backend — FastAPI

Python + FastAPI backend for the PrimeHomes Realty Lead Bot.

## Responsibilities

- REST API (`/api/v1/...`)
- Request validation (Pydantic)
- Business logic & lead scoring
- PostgreSQL persistence (SQLAlchemy + Alembic)
- Communication with n8n
- AI service orchestration (extraction + response generation)

## Structure

```text
backend/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── routes/
├── tests/
├── alembic/
├── requirements.txt
└── Dockerfile
```

## Local Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

- Health: http://localhost:8000/health
- Docs:   http://localhost:8000/docs
