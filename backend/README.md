# Backend — FastAPI

Python + FastAPI backend for the PrimeHomes Realty Lead Bot.

## Responsibilities

- REST API (`/api/v1/...`)
- Request validation (Pydantic)
- Business logic & lead scoring
- PostgreSQL persistence (SQLAlchemy + Alembic)
- Communication with n8n
- AI service orchestration

## Structure

```text
backend/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database/
│   │   └── connection.py
│   ├── models/
│   │   ├── enums.py
│   │   ├── customer.py
│   │   ├── lead.py
│   │   ├── conversation.py
│   │   └── __init__.py
│   ├── schemas/
│   ├── services/
│   └── routes/
├── alembic/
├── alembic.ini
├── requirements.txt
└── README.md
```

## Database Models (Phase 2)

Implemented according to the Database Design specification:

| Table                  | Purpose                          |
|------------------------|----------------------------------|
| `customers`            | Customer identity & contact      |
| `leads`                | Sales opportunities              |
| `property_requirements`| Property preferences             |
| `conversations`        | Chat sessions                    |
| `messages`             | Individual messages              |
| `lead_qualifications`  | Scoring results                  |
| `sales_reps`           | Sales team members               |
| `lead_assignments`     | Assignment history               |
| `lead_status_history`  | Status audit trail               |
| `follow_ups`           | Follow-up tasks                  |
| `ai_extractions`       | AI structured output audit       |

## Local Development

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Ensure PostgreSQL is running (docker compose up -d postgres)
# Then create the first migration:
alembic revision --autogenerate -m "initial schema"
alembic upgrade head

# Start the API
uvicorn app.main:app --reload --port 8000
```

- Health: http://localhost:8000/health
- Docs:   http://localhost:8000/docs
