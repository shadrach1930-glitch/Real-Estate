# PrimeHomes Realty Real Estate Lead Bot

## Deployment & DevOps Specification

Document ID: PRH-DEVOPS-012  
Version: 1.0  
Status: Approved for Development

---

# 1. Purpose

This document defines how the PrimeHomes Realty Real Estate Lead Bot will be configured, developed, tested, deployed, monitored, backed up, and maintained.

The deployment strategy should support:

```text
Local Development
       ↓
Testing
       ↓
Staging
       ↓
Production
```

---

# 2. Technology Stack

## Frontend

- React
- JavaScript/TypeScript as selected during implementation
- Modern browser-based UI

## Backend

- Python
- FastAPI
- Pydantic
- PostgreSQL

## Automation

- n8n

## AI

- Configurable LLM provider
- Model selected through environment configuration

## Operational Data

- PostgreSQL
- Google Sheets for secondary operational visibility

---

# 3. Environment Strategy

The project should maintain separate environments.

### Development

Used by developers for active development.

### Staging

Used for integration and pre-production testing.

### Production

Used by real customers and sales staff.

Credentials must never be shared between environments.

---

# 4. Configuration

Application configuration should be environment-based.

Example:

```text
APP_ENV=development

DATABASE_URL=...

AI_PROVIDER=google
AI_MODEL=...
AI_TEMPERATURE=0.2

N8N_BASE_URL=...
N8N_WEBHOOK_SECRET=...

FRONTEND_URL=...
```

The actual secret values must not be committed to Git.

---

# 5. Repository Structure

The project repository should follow a structure similar to:

```text
primehomes-lead-bot/
│
├── frontend/
│
├── backend/
│
├── n8n/
│
├── docs/
│
├── tests/
│
├── .env.example
├── .gitignore
├── README.md
└── docker-compose.yml
```

---

# 6. Local Development

A developer should be able to start the required services locally.

Recommended services:

```text
React
FastAPI
PostgreSQL
n8n
```

A local development configuration may use Docker Compose to simplify service startup.

---

# 7. Backend Startup

FastAPI should run locally on:

```text
http://localhost:8000
```

API prefix:

```text
/api/v1
```

Documentation:

```text
/docs
/redoc
```

Health endpoint:

```text
GET /health
```

---

# 8. Frontend Startup

The React application should run on a development port such as:

```text
http://localhost:5173
```

The frontend should communicate with FastAPI rather than directly accessing PostgreSQL.

---

# 9. Database Setup

PostgreSQL should be initialized using migrations.

The implementation should use a migration framework such as Alembic.

Database changes must not be performed manually in production unless required for emergency recovery.

Recommended process:

```text
Modify model
   ↓
Create migration
   ↓
Review migration
   ↓
Run tests
   ↓
Apply migration
```

---

# 10. n8n Deployment

n8n may initially run locally during development.

Production deployment should use:

- Secure authentication
- HTTPS
- Persistent storage
- Secure credentials
- Controlled webhook access
- Execution monitoring
- Error workflows

Production n8n credentials must be separate from development credentials.

---

# 11. Docker

Docker is recommended for consistent deployment.

Potential services:

```text
frontend
backend
postgres
n8n
```

Development can use:

```text
docker compose up
```

Production deployment may use a managed container platform or VPS/cloud infrastructure depending on operational requirements.

---

# 12. CI/CD

The project should eventually implement continuous integration.

Every pull request should ideally run:

```text
Lint
   ↓
Unit Tests
   ↓
Integration Tests
   ↓
Build
```

Deployment should only proceed if required checks pass.

---

# 13. Git Strategy

Recommended branches:

```text
main
develop
feature/*
fix/*
```

Examples:

```text
feature/lead-chat
feature/lead-scoring
feature/n8n-workflow
fix/ai-validation
```

Commit messages should clearly describe changes.

---

# 14. Deployment Process

Recommended deployment flow:

```text
Developer
    ↓
Feature Branch
    ↓
Pull Request
    ↓
Automated Tests
    ↓
Code Review
    ↓
Merge
    ↓
Staging
    ↓
Acceptance Testing
    ↓
Production
```

---

# 15. Database Deployment

Database migrations must be applied before application functionality that depends on them.

Production database changes must be:

- Version controlled
- Tested
- Reversible where practical
- Backed up before risky migrations

---

# 16. Monitoring

The system should monitor:

### Backend

- API availability
- Response time
- Error rate
- Database connectivity

### n8n

- Workflow failures
- Execution duration
- Failed executions
- Queue/backlog where applicable

### AI

- Provider failures
- Timeout rate
- Invalid responses
- Token usage
- Processing time

### Database

- Availability
- Storage
- Connection count
- Query performance

---

# 17. Health Checks

The system should expose health checks.

Example:

```text
GET /health
```

The health response should indicate whether the application is operational.

A deeper readiness check may verify:

- Database connectivity
- Required configuration
- Critical dependencies

---

# 18. Backup Strategy

Production data should be backed up automatically.

At minimum:

- Daily database backup
- Appropriate retention
- Secure backup storage
- Restore testing

For higher reliability, point-in-time recovery should be considered.

---

# 19. Rollback Strategy

If a deployment causes a critical failure:

```text
Detect failure
   ↓
Stop rollout
   ↓
Rollback application
   ↓
Verify database compatibility
   ↓
Restore service
   ↓
Investigate
```

Database migrations that are difficult to reverse must be designed using backward-compatible deployment patterns.

---

# 20. Production Security

Production must use:

- HTTPS
- Secure environment variables
- Restricted database access
- Authentication
- Authorization
- CORS restrictions
- Rate limiting
- Secure cookies/tokens where applicable
- Firewall/network restrictions

Debug mode must be disabled in production.

---

# 21. CORS

Development may permit the local React application.

Production should allow only the approved frontend origin.

Example concept:

```text
Development:
http://localhost:5173

Production:
https://app.primehomes.example
```

The actual production domain will be configured during deployment.

---

# 22. Domain & HTTPS

Production services should use HTTPS.

Potential architecture:

```text
Internet
   ↓
HTTPS
   ↓
Reverse Proxy
   ↓
FastAPI
   ↓
PostgreSQL
```

n8n should also be exposed securely if external webhooks require public access.

---

# 23. Environment Variables

Required configuration should be documented in `.env.example`.

Example categories:

```text
Application
Database
AI
n8n
Authentication
CORS
Notifications
Logging
```

Actual credentials remain outside version control.

---

# 24. Logging

Production logs should be structured.

Every important request should be traceable using:

```text
request_id
conversation_id
lead_id
workflow_id
execution_id
```

Logs should have appropriate retention.

---

# 25. Performance

Initial performance targets should include:

- Fast API response for normal requests
- Asynchronous processing for slow AI operations where appropriate
- Database indexes on frequently queried fields
- Pagination for lead lists
- Avoiding unnecessary AI calls
- Efficient n8n workflows

The system should be designed so that increasing from dozens to hundreds of daily messages does not require rewriting the architecture.

---

# 26. Deployment Documentation

The repository must contain a README covering:

1. Prerequisites
2. Installation
3. Environment variables
4. Database setup
5. Migration commands
6. Backend startup
7. Frontend startup
8. n8n setup
9. Testing
10. Deployment
11. Troubleshooting

---

# 27. Definition of Done

Deployment and DevOps implementation is complete when:

- Local development environment works
- PostgreSQL setup is documented
- Database migrations work
- FastAPI starts correctly
- React starts correctly
- n8n workflows are importable/configured
- Environment variables are documented
- Secrets are excluded from Git
- Automated tests run successfully
- Health checks work
- Production deployment procedure is documented
- Backup procedure exists
- Rollback procedure exists
- Monitoring/logging is configured
- HTTPS is enabled in production