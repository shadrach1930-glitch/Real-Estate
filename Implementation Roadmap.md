# PrimeHomes Realty Real Estate Lead Bot

## Implementation Roadmap

Document ID: PRH-ROADMAP-013  
Version: 1.0  
Status: Approved for Development

---

# 1. Purpose

This roadmap converts the PrimeHomes Realty Real Estate Lead Bot documentation into an executable development plan.

The implementation should proceed incrementally rather than attempting to build the entire system at once.

The goal is to create a working vertical slice early, then expand it into the complete platform.

---

# 2. Implementation Strategy

The recommended sequence is:

```text
Project Setup
      ↓
Database
      ↓
FastAPI
      ↓
React Chat
      ↓
n8n
      ↓
AI
      ↓
Lead Qualification
      ↓
Sales Dashboard
      ↓
Follow-ups
      ↓
Testing
      ↓
Deployment
```

---

# 3. Phase 1 — Project Initialization

## Objectives

Create the project structure and development environment.

## Tasks

- Create Git repository
- Create frontend project
- Create backend project
- Create documentation directory
- Create `.gitignore`
- Create `.env.example`
- Configure Python environment
- Configure React environment
- Configure PostgreSQL
- Configure n8n
- Create initial README

## Deliverable

A clean repository where all core services can be started locally.

---

# 4. Phase 2 — Database Implementation

## Objectives

Implement PostgreSQL according to the database specification.

## Tasks

Create models for:

- Customers
- Leads
- Property requirements
- Conversations
- Messages
- Lead qualifications
- Sales representatives
- Lead assignments
- Lead status history
- Follow-ups
- AI extractions

## Additional Tasks

- Configure SQLAlchemy
- Configure Alembic
- Create initial migration
- Add indexes
- Test database connection
- Test CRUD operations

## Deliverable

A working PostgreSQL schema that can persist the complete lead lifecycle.

---

# 5. Phase 3 — FastAPI Foundation

## Objectives

Build the backend API.

## Tasks

Create:

```text
main.py
config.py
database/
models/
schemas/
services/
routes/
```

Implement:

```text
GET /health
POST /api/v1/chat
GET /api/v1/conversations/{id}

GET /api/v1/leads
POST /api/v1/leads
GET /api/v1/leads/{id}
PATCH /api/v1/leads/{id}

POST /api/v1/leads/{id}/qualify
POST /api/v1/leads/{id}/assign

GET /api/v1/leads/{id}/history

POST /api/v1/leads/{id}/follow-ups
GET /api/v1/leads/{id}/follow-ups
PATCH /api/v1/follow-ups/{id}

POST /api/v1/webhooks/n8n
GET /api/v1/dashboard/summary
```

## Deliverable

A functioning REST API with validation and consistent error responses.

---

# 6. Phase 4 — Customer Chat Interface

## Objectives

Build the first usable customer experience.

## Tasks

Implement:

- Chat page
- Message bubbles
- Message input
- Send button
- Loading state
- Typing indicator
- Error state
- Quick actions
- Conversation state

The customer should be able to send:

> "I'm looking for a 3-bedroom apartment in Lekki with a budget of ₦80 million."

The message should reach FastAPI.

## Deliverable

A functioning React → FastAPI customer chat flow.

---

# 7. Phase 5 — n8n Integration

## Objectives

Connect FastAPI to the automation layer.

## Tasks

Implement:

```text
FastAPI
   ↓
n8n webhook
   ↓
Workflow
   ↓
FastAPI callback
```

Create the initial workflows:

```text
WF-001 Receive Customer Message
WF-002 Process Conversation
WF-003 AI Lead Extraction
```

Add:

- Webhook authentication
- Error handling
- Request IDs
- Execution tracking

## Deliverable

A customer message can successfully travel through FastAPI and n8n.

---

# 8. Phase 6 — AI Lead Extraction

## Objectives

Enable natural-language understanding.

## Tasks

Implement AI extraction for:

- Intent
- Transaction type
- Property type
- Bedrooms
- Location
- Budget
- Currency
- Timeline
- Customer information
- Additional requirements
- Missing information
- Confidence

The AI must return structured JSON.

Example:

```json
{
  "intent": "BUY",
  "transaction_type": "BUY",
  "property_type": "APARTMENT",
  "bedrooms": 3,
  "location": "Lekki",
  "budget_min": 80000000,
  "budget_max": 80000000,
  "currency": "NGN",
  "timeline": "UNKNOWN",
  "confidence": 0.94
}
```

## Deliverable

Reliable structured extraction from natural-language messages.

---

# 9. Phase 7 — Validation & Normalization

## Objectives

Ensure AI output is safe and consistent.

## Tasks

Implement:

- JSON validation
- Schema validation
- Enum validation
- Currency normalization
- Budget normalization
- Location preservation
- Confidence handling
- Ambiguity detection

The backend must reject or safely handle invalid AI output.

## Deliverable

AI output becomes validated application data.

---

# 10. Phase 8 — Lead Qualification

## Objectives

Implement deterministic lead scoring.

Scoring:

```text
Phone             +10
Budget            +20
Location          +15
Property Type     +15
Buying Soon       +25
Clear Requirements+15
```

Maximum:

```text
100
```

Classification:

```text
80–100  HOT
50–79   WARM
0–49    COLD
```

This logic belongs in the backend.

## Deliverable

Every qualifying lead receives a deterministic score and temperature.

---

# 11. Phase 9 — Lead Persistence

## Objectives

Persist extracted information.

Processing:

```text
Customer Message
      ↓
AI Extraction
      ↓
Validation
      ↓
Lead Update
      ↓
Qualification
      ↓
PostgreSQL
```

Implement idempotency to prevent duplicate records.

## Deliverable

A complete customer enquiry is persisted as a structured lead.

---

# 12. Phase 10 — Missing Information Collection

## Objectives

Allow the bot to progressively collect missing information.

For example:

Customer:

> "I want to buy a house."

Bot:

> "Absolutely. Which area are you interested in, and what budget range should I work with?"

The bot should not ask for every field at once.

Priority should be given to information that materially improves qualification.

## Deliverable

The conversation progressively builds a complete lead profile.

---

# 13. Phase 11 — Customer Response Generation

## Objectives

Generate useful conversational responses.

The AI should:

- Acknowledge the customer
- Confirm captured information
- Ask relevant missing questions
- Avoid inventing listings
- Avoid inventing prices
- Avoid claiming availability
- Escalate when necessary

## Deliverable

A natural conversational experience.

---

# 14. Phase 12 — Google Sheets Synchronization

## Objectives

Create operational visibility for the sales team.

Sync:

```text
PostgreSQL
     ↓
n8n
     ↓
Google Sheets
```

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

## Deliverable

Sales can view operational lead data in Google Sheets.

---

# 15. Phase 13 — Sales Notifications

## Objectives

Notify sales when important leads arrive.

Notification should include:

- Customer
- Contact information
- Property requirements
- Budget
- Location
- Lead score
- Lead temperature
- Timeline
- Conversation reference

Hot leads should receive priority notification.

## Deliverable

Sales receives actionable lead notifications.

---

# 16. Phase 14 — Sales Dashboard

## Objectives

Build the internal lead-management interface.

Dashboard metrics:

```text
Total Leads
New Leads
Hot Leads
Warm Leads
Qualified Leads
Converted Leads
Pending Follow-ups
```

Lead list:

```text
Lead
Property
Location
Budget
Score
Temperature
Status
Assigned To
Created
```

Lead details should show:

- Customer information
- Requirements
- Score
- Status
- Conversation
- Follow-ups
- Assignment
- History

## Deliverable

Sales team can manage leads through the web interface.

---

# 17. Phase 15 — Follow-Up Automation

## Objectives

Prevent qualified leads from being forgotten.

n8n should periodically identify leads requiring follow-up.

Example:

```text
Schedule Trigger
      ↓
Find Pending Follow-ups
      ↓
Check Lead Status
      ↓
Notify Sales
      ↓
Update Follow-up State
```

The system should not send inappropriate follow-ups to:

- Converted leads
- Lost leads
- Closed leads

## Deliverable

Follow-up management works automatically.

---

# 18. Phase 16 — Human Escalation

Escalate when:

- Customer requests a human
- AI confidence is low
- Enquiry is complex
- Lead is high-value
- Customer is dissatisfied
- System cannot safely answer
- Property availability must be verified

Example:

```text
Customer
   ↓
AI detects HUMAN_REQUEST
   ↓
Lead marked for escalation
   ↓
Sales notification
   ↓
Human follow-up
```

## Deliverable

Customers can smoothly transition from bot to human sales support.

---

# 19. Phase 17 — Testing & QA

Testing should cover:

### Unit Tests

- Lead scoring
- Validation
- Normalization
- Business rules

### Integration Tests

- FastAPI + PostgreSQL
- FastAPI + n8n
- n8n + AI
- n8n + Google Sheets

### End-to-End Tests

```text
Customer
 → React
 → FastAPI
 → n8n
 → AI
 → PostgreSQL
 → Google Sheets
 → Notification
 → Response
```

### Security Tests

- Unauthorized access
- Invalid input
- Rate limiting
- Prompt injection
- Secret exposure
- Duplicate requests

---

# 20. Phase 18 — Performance Optimization

After functional correctness is established:

- Optimize database queries
- Add required indexes
- Reduce unnecessary AI calls
- Improve response times
- Add pagination
- Optimize n8n workflows
- Review logging volume
- Review API throughput

Optimization should not happen before the core workflow is stable.

---

# 21. Phase 19 — Deployment

Deployment sequence:

```text
Local
  ↓
Staging
  ↓
Acceptance Testing
  ↓
Production
```

Production requirements:

- HTTPS
- Secure credentials
- PostgreSQL backups
- Monitoring
- Logging
- Rate limiting
- Authentication
- CORS restrictions
- Error handling
- Recovery procedure

---

# 22. Phase 20 — Production Validation

Before going live, verify:

### Customer Flow

- Customer can start conversation
- Messages are persisted
- AI extracts requirements
- Missing information is collected
- Response is generated

### Lead Flow

- Lead is created
- Score is calculated
- Temperature is assigned
- Status is correct
- Lead can be assigned

### Sales Flow

- Sales receives notifications
- Dashboard displays lead
- Conversation is accessible
- Follow-up can be created

### Reliability

- Duplicate messages are handled
- AI failures do not lose leads
- Google Sheets failure does not lose leads
- n8n failure is detected
- Database backup works

---

# 23. Recommended Development Order

The actual coding sequence should be:

```text
1. Repository setup
2. Environment configuration
3. PostgreSQL
4. Database models
5. Alembic migrations
6. FastAPI foundation
7. Lead CRUD
8. Conversation/message APIs
9. React chat UI
10. React API integration
11. n8n webhook
12. AI extraction
13. AI validation
14. Lead scoring
15. Missing information flow
16. Response generation
17. Google Sheets sync
18. Notifications
19. Sales dashboard
20. Follow-ups
21. Human escalation
22. Testing
23. Security hardening
24. Deployment
25. Production validation
```

---

# 24. Definition of Done

The project is considered ready for its first production release when:

- Customer chat works
- Customer messages are persisted
- AI extraction works reliably
- AI output is validated
- Lead scoring works deterministically
- Leads are stored in PostgreSQL
- Google Sheets synchronization works
- Sales notifications work
- Sales dashboard works
- Follow-ups work
- Human escalation works
- Error handling works
- Security controls are implemented
- Automated tests pass
- Backups are configured
- Deployment is documented
- Production monitoring is active

---

# 25. First Production Milestone

The first milestone should not attempt every advanced feature.

The recommended MVP is:

```text
Customer
   ↓
React Chat
   ↓
FastAPI
   ↓
n8n
   ↓
AI Extraction
   ↓
Validation
   ↓
Lead Scoring
   ↓
PostgreSQL
   ↓
Google Sheets
   ↓
Sales Notification
   ↓
Customer Response
```

Once this vertical slice is stable, the team can add:

```text
Sales Dashboard
Follow-ups
Human Escalation
Advanced Analytics
Property Inventory Integration
Automated Campaigns
```

This approach minimizes risk while producing a usable system early.