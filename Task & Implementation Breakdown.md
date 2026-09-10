# PRIMEHOMES REALTY REAL ESTATE LEAD BOT

## TASK & IMPLEMENTATION BREAKDOWN

**Document ID:** PRH-IMP-009  
**Version:** 1.0  
**Status:** Ready for Development

---

# 1. Purpose

This document converts the approved project specifications into concrete development tasks.

Every task should have:

- A clear owner
- A defined dependency
- An expected output
- Acceptance criteria
- A completion state

Development should proceed sequentially where dependencies require it, while independent tasks may be developed in parallel.

---

# 2. Development Priority

Priority levels:

- **P0 — Critical:** Required for MVP
- **P1 — High:** Required for a complete MVP
- **P2 — Medium:** Important but can follow MVP
- **P3 — Future:** Enhancement

---

# 3. Phase 0 — Project Initialization

## IMP-001 — Create project repository
**Priority:** P0

Create the project repository and establish the root structure.

```text
primehomes-realty-bot/
├── frontend/
├── backend/
├── n8n/
├── docs/
├── tests/
└── README.md
```

**Acceptance Criteria**
- Repository exists.
- README exists.
- Folder structure is documented.

---

## IMP-002 — Configure Git

- Create `.gitignore`.
- Establish main/development branch strategy.
- Prevent secrets from entering Git.
- Add environment examples.

---

## IMP-003 — Create environment configuration

Create:

```text
.env
.env.example
```

Variables should include:

```text
DATABASE_URL
AI_PROVIDER
AI_MODEL
AI_API_KEY
N8N_BASE_URL
N8N_WEBHOOK_URL
GOOGLE_SHEETS_CREDENTIAL
```

Secrets must never be committed.

---

# 4. Phase 1 — Backend Foundation

## IMP-004 — Initialize FastAPI

Create:

```text
backend/
app/
main.py
config.py
```

**Acceptance Criteria**
- FastAPI starts successfully.
- `/health` returns HTTP 200.
- `/docs` is accessible.

---

## IMP-005 — Configure application settings

Implement environment-based configuration.

---

## IMP-006 — Configure PostgreSQL connection

Implement:

- Database connection
- Session management
- Connection pooling
- Environment configuration

---

## IMP-007 — Configure migrations

Use a migration system such as Alembic.

**Acceptance Criteria**
- Initial migration can be generated.
- Database can be upgraded from an empty state.

---

# 5. Phase 2 — Database Implementation

## IMP-008 — Create customer model

Implement `customers`.

---

## IMP-009 — Create lead model

Implement `leads`.

---

## IMP-010 — Create property requirements model

Implement `property_requirements`.

---

## IMP-011 — Create conversation and message models

Implement:

```text
conversations
messages
```

---

## IMP-012 — Create qualification model

Implement `lead_qualifications`.

---

## IMP-013 — Create sales and assignment models

Implement:

```text
sales_reps
lead_assignments
```

---

## IMP-014 — Create status history

Implement `lead_status_history`.

---

## IMP-015 — Create follow-up model

Implement `follow_ups`.

---

## IMP-016 — Create AI extraction model

Implement `ai_extractions`.

---

## IMP-017 — Add indexes and constraints

Important indexes:

- customer email
- customer phone
- lead status
- lead temperature
- lead score
- created_at
- conversation ID
- message external ID

---

# 6. Phase 3 — Backend Services

## IMP-018 — Lead service

Implement:

- Create lead
- Retrieve lead
- Update lead
- List leads
- Lead status changes

---

## IMP-019 — Conversation service

Implement:

- Create conversation
- Store messages
- Retrieve context
- Retrieve conversation history

---

## IMP-020 — Qualification service

Implement the agreed scoring rules:

```text
Phone       +10
Budget      +20
Location    +15
Property    +15
Buying soon +25
Requirements +15
```

Classification:

```text
80–100 = HOT
50–79  = WARM
0–49   = COLD
```

---

## IMP-021 — Follow-up service

Implement:

- Create follow-up
- Update follow-up
- Complete follow-up
- List pending follow-ups

---

# 7. Phase 4 — API Implementation

## IMP-022 — Health API

```text
GET /health
```

---

## IMP-023 — Chat API

```text
POST /api/v1/chat
```

Responsibilities:

- Validate message
- Create/retrieve conversation
- Persist message
- Trigger processing
- Return appropriate response

---

## IMP-024 — Lead APIs

Implement:

```text
GET    /api/v1/leads
POST   /api/v1/leads
GET    /api/v1/leads/{id}
PATCH  /api/v1/leads/{id}
POST   /api/v1/leads/{id}/qualify
POST   /api/v1/leads/{id}/assign
GET    /api/v1/leads/{id}/history
```

---

## IMP-025 — Follow-up APIs

Implement:

```text
POST  /api/v1/leads/{id}/follow-ups
GET   /api/v1/leads/{id}/follow-ups
PATCH /api/v1/follow-ups/{id}
```

---

## IMP-026 — Dashboard API

Implement:

```text
GET /api/v1/dashboard/summary
```

---

## IMP-027 — n8n webhook API

Implement:

```text
POST /api/v1/webhooks/n8n
```

Include request validation and idempotency.

---

# 8. Phase 5 — Frontend Foundation

## IMP-028 — Initialize React application

Implement:

```text
frontend/src/
components/
pages/
services/
hooks/
utils/
```

---

## IMP-029 — Configure routing

Routes:

```text
/
/dashboard
/leads
/leads/:id
/follow-ups
```

---

## IMP-030 — Configure API client

Create:

```text
services/api.js
```

The frontend communicates with FastAPI only.

---

# 9. Phase 6 — Customer Chat

## IMP-031 — Build ChatWindow

---

## IMP-032 — Build MessageBubble

Support:

- Customer messages
- Bot messages
- System states

---

## IMP-033 — Build MessageInput

Support:

- Text entry
- Send
- Loading state
- Error state

---

## IMP-034 — Build typing indicator

---

## IMP-035 — Build quick actions

Examples:

```text
Buy a property
Rent a property
Find land
Speak to an agent
```

---

# 10. Phase 7 — Sales Dashboard

## IMP-036 — Dashboard summary

Display:

```text
Total Leads
New Leads
Hot Leads
Warm Leads
Qualified Leads
Converted Leads
Pending Follow-ups
```

---

## IMP-037 — Lead table

Columns:

```text
Lead
Property
Location
Budget
Score
Temperature
Status
Assigned Rep
Created
```

---

## IMP-038 — Lead filtering

Filters:

- Status
- Temperature
- Intent
- Assignment

---

## IMP-039 — Lead details page

Display:

- Customer
- Requirements
- Qualification
- Status
- Conversation
- Assignment
- Follow-ups

---

## IMP-040 — Follow-up interface

Implement:

- Create
- View
- Edit
- Complete

---

# 11. Phase 8 — AI Implementation

## IMP-041 — Implement AI provider service

Create:

```text
services/ai_service.py
```

The provider/model must be configurable.

---

## IMP-042 — Implement extraction prompt

Create versioned:

```text
lead-extraction-v1.0
```

---

## IMP-043 — Implement structured output validation

Reject malformed responses.

---

## IMP-044 — Implement normalization

Support:

- NGN
- Nigerian currency expressions
- Bedroom terminology
- Property types
- Timeline terminology
- Location expressions

---

## IMP-045 — Implement missing-information logic

The AI must avoid repeating already answered questions.

---

## IMP-046 — Implement response generation

Create:

```text
response-generation-v1.0
```

---

## IMP-047 — Implement AI guardrails

Prevent:

- Invented properties
- Invented prices
- Invented availability
- Prompt leakage
- Unsupported promises

---

# 12. Phase 9 — n8n Implementation

Implement the approved workflows:

```text
WF-001 Receive Customer Message
WF-002 Process Conversation
WF-003 AI Lead Extraction
WF-004 Validate Lead Data
WF-005 Collect Missing Information
WF-006 Qualify Lead
WF-007 Store Lead
WF-008 Google Sheets Sync
WF-009 Sales Notification
WF-010 Generate Customer Response
WF-011 Follow-Up Automation
WF-012 Error Handling
```

---

# 13. Phase 10 — Google Sheets Integration

Create the operational sheet.

Columns:

```text
Lead ID
Customer Name
Email
Phone
Property Type
Bedrooms
Location
Budget
Currency
Transaction Type
Timeline
Intent
Score
Temperature
Status
Assigned Sales Rep
Created At
Updated At
```

PostgreSQL remains authoritative.

---

# 14. Phase 11 — Notification System

Implement sales notifications for:

- HOT leads
- Human escalation
- High-value enquiries
- Assignment
- Important follow-ups

---

# 15. Phase 12 — Follow-Up Automation

n8n scheduled workflow:

```text
Schedule
 ↓
Find pending follow-ups
 ↓
Check due date
 ↓
Notify sales representative
 ↓
Record notification
```

No infinite notification loops.

---

# 16. Phase 13 — Integration

Connect:

```text
React
 ↓
FastAPI
 ↓
n8n
 ↓
AI
 ↓
PostgreSQL
 ↓
Google Sheets
 ↓
Sales notification
```

Perform end-to-end testing.

---

# 17. Phase 14 — Completion Criteria

The MVP is complete when:

- Customer can submit an enquiry.
- Conversation is persisted.
- AI extracts structured information.
- Missing information is requested.
- Lead is created/updated.
- Lead score is calculated.
- Lead temperature is calculated.
- Lead is stored in PostgreSQL.
- Google Sheets receives the lead.
- Sales team receives appropriate notification.
- Customer receives a response.
- Follow-ups can be created.
- Sales team can manage leads.
- Errors are logged.
- Duplicate processing is prevented.
- Core tests pass.

---

# 18. Dependency Order

The critical development path is:

```text
Repository
 ↓
Backend foundation
 ↓
Database
 ↓
Backend services
 ↓
APIs
 ↓
n8n
 ↓
AI
 ↓
Frontend
 ↓
Integration
 ↓
Testing
 ↓
Security
 ↓
Deployment
```

Some frontend work can happen in parallel with backend development once the API contracts are stable.

---

# 19. Definition of Done

A task is not considered complete merely because code exists.

It is complete when:

1. Code is implemented.
2. It follows the project architecture.
3. It has appropriate validation.
4. Tests pass.
5. Error handling exists.
6. Documentation is updated where necessary.
7. No secrets are committed.
8. Acceptance criteria are satisfied.