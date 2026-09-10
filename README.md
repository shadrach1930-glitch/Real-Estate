# PrimeHomes Realty — Real Estate Lead Bot

Intelligent lead-management system that turns unstructured customer property enquiries into structured, qualified, actionable sales leads.

> **Every customer enquiry should be captured, understood, qualified, responded to, and made actionable for the sales team.**

## Architecture Overview

```text
Customer
   ↓
React Chat UI
   ↓
FastAPI (Backend + Business Logic)
   ↓
n8n (Workflow Orchestration)
   ↓
┌──────────────┬──────────────┬─────────────────┐
│      AI      │  PostgreSQL  │  Integrations   │
│ (Extraction  │  (Source of  │  Google Sheets  │
│  + Response) │   Truth)     │  Notifications  │
└──────────────┴──────────────┴─────────────────┘
   ↓
Sales Team
```

**Core principle:**  
*AI interprets. The backend validates. The database stores. Business logic decides.*

## Repository Structure

```text
Real-Estate/
├── frontend/                 # React customer chat + sales dashboard
├── backend/                  # FastAPI + business logic + models
├── n8n/                      # Workflow definitions & documentation
├── docs/                     # All approved foundational specifications
├── tests/                    # Cross-cutting / e2e tests
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md
```

## Tech Stack

| Layer            | Technology              |
|------------------|-------------------------|
| Frontend         | React (Vite)            |
| Backend          | Python + FastAPI        |
| Database         | PostgreSQL              |
| Automation       | n8n                     |
| AI               | Configurable LLM        |
| Operational View | Google Sheets           |

## Quick Start (Local Development)

1. **Clone & configure**
   ```bash
   git clone https://github.com/shadrach1930-glitch/Real-Estate.git
   cd Real-Estate
   cp .env.example .env
   # Edit .env with your values
   ```

2. **Start services**
   ```bash
   docker compose up -d postgres
   # Then start backend, frontend, n8n as needed
   ```

3. **Backend**
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate   # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```
   API docs: http://localhost:8000/docs

4. **Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   Chat UI: http://localhost:5173

## Documentation

All approved specifications live in the [`docs/`](./docs) folder:

- Product Requirements Document (PRD)
- System Design & Technical Architecture
- Database Design & Data Model
- API Specification
- UI/UX Specification
- Data Flow & Workflow Specification
- n8n Workflow Specification
- AI & Prompt Engineering Specification
- Security & Reliability Specification
- Testing & QA Specification
- Deployment & DevOps Specification
- Implementation Roadmap
- Task & Implementation Breakdown

## Project Status

**Phase 0 — Project Initialization** (current)

Scaffolding complete. Next steps follow the Implementation Roadmap:

1. Database models + Alembic migrations
2. FastAPI foundation + core endpoints
3. React chat interface
4. n8n + AI extraction
5. Lead qualification & persistence
6. Sales dashboard & follow-ups

## License

MIT
