# SYSTEM DESIGN & TECHNICAL ARCHITECTURE

## PrimeHomes Realty — Real Estate Lead Bot

**Document Version:** 1.0  
**Status:** Draft  
**Project Phase:** System Design  
**Based On:** Product Requirements Document v1.0  
**Date:** September 2026

---

# 1. Document Purpose

This document defines the technical architecture and system design for the PrimeHomes Realty Real Estate Lead Bot.

The purpose is to establish:

- System components.
- Responsibilities of each component.
- Data flow.
- Communication between services.
- API boundaries.
- Automation responsibilities.
- AI responsibilities.
- Database responsibilities.
- Integration strategy.
- Error-handling strategy.
- Security considerations.
- Deployment considerations.

This document serves as the technical blueprint that developers will use during implementation.

---

# 2. System Overview

The PrimeHomes Realty Lead Bot is a multi-component business automation system.

At a high level:

```text
                    CUSTOMER
                        │
                        ▼
               ┌─────────────────┐
               │  React Frontend │
               │   Chat / Forms  │
               └────────┬────────┘
                        │
                        ▼
               ┌─────────────────┐
               │   FastAPI API   │
               │ Python Backend  │
               └────────┬────────┘
                        │
                        ▼
               ┌─────────────────┐
               │       n8n       │
               │ Workflow Engine │
               └────────┬────────┘
                        │
              ┌─────────┼─────────┐
              │         │         │
              ▼         ▼         ▼
             AI        SQL     Integrations
              │         │         │
              │         │         ├── Google Sheets
              │         │         ├── Notifications
              │         │         └── Future CRM
              │         │
              └─────────┴─────────┘
                        │
                        ▼
                  SALES TEAM
```

---

# 3. Architecture Principles

The system will follow several core engineering principles.

## 3.1 Separation of Responsibilities

Each technology should solve the problem it is best suited for.

```text
React
→ User interface

FastAPI
→ Backend/API/business services

n8n
→ Workflow orchestration/integrations

AI
→ Language understanding/generation

SQL
→ Persistent application data

Google Sheets
→ Operational visibility/integration
```

No component should unnecessarily take responsibility for another component's job.

---

# 4. Architectural Style

The MVP will use a **modular service-oriented architecture**.

It is not necessary to introduce microservices at this stage.

Instead, we will maintain clearly separated components:

```text
Frontend
Backend
Automation
AI
Database
Integrations
```

This keeps the system simple enough for the MVP while allowing future expansion.

---

# 5. Major System Components

## 5.1 React Frontend

The frontend is the customer-facing application.

Responsibilities:

- Display chat interface.
- Accept customer messages.
- Display bot responses.
- Collect customer information.
- Display loading states.
- Display errors.
- Maintain conversation/session state.
- Communicate with FastAPI.

The frontend should not contain sensitive API credentials.

---

# 6. FastAPI Backend

FastAPI provides the application's backend API.

Responsibilities:

- Receive frontend requests.
- Validate incoming data.
- Manage API contracts.
- Generate/maintain conversation identifiers.
- Communicate with n8n.
- Perform custom business logic.
- Interact with SQL where appropriate.
- Handle backend-level authentication/authorization.
- Return structured responses to React.

FastAPI acts as the controlled entry point between the frontend and backend services.

---

# 7. n8n Automation Layer

n8n is the workflow orchestration engine.

It coordinates processes such as:

```text
Receive Lead
     ↓
Validate
     ↓
AI Extraction
     ↓
Business Rules
     ↓
Lead Scoring
     ↓
Database
     ↓
Google Sheets
     ↓
Notification
     ↓
Customer Response
```

n8n should primarily coordinate operations rather than becoming a giant application containing all business logic.

---

# 8. AI Layer

AI is responsible for understanding natural-language customer communication.

Primary responsibilities:

- Intent detection.
- Information extraction.
- Requirement extraction.
- Missing-field detection.
- Conversation summarization.
- Response generation.

AI output should be structured whenever possible.

Example:

```json
{
  "intent": "buy",
  "property_type": "apartment",
  "bedrooms": 3,
  "location": "Lekki",
  "budget": 80000000,
  "timeline": "within_3_months"
}
```

The application should validate this output before using it.

---

# 9. SQL Database

The SQL database is the **primary system of record**.

It stores:

- Leads.
- Customers.
- Conversations.
- Messages.
- Lead requirements.
- Scores.
- Statuses.
- Assignments.
- Follow-ups.
- Audit information.

Google Sheets should not replace the SQL database.

---

# 10. Google Sheets

Google Sheets provides an operational data view.

Potential uses:

- Sales team visibility.
- Simple manual inspection.
- Lead monitoring.
- n8n integration.
- Demonstration.
- Lightweight reporting.

The SQL database remains authoritative for application data.

---

# 11. External Integrations

n8n will be responsible for communicating with external services where practical.

Possible integrations:

```text
Google Sheets
Email
WhatsApp
Slack
CRM
Calendar
Other APIs
```

The exact integrations depend on the client's final requirements.

---

# 12. High-Level Data Flow

The main customer flow is:

```text
Customer
   │
   │ Message
   ▼
React
   │
   │ HTTP Request
   ▼
FastAPI
   │
   │ Webhook/API Request
   ▼
n8n
   │
   ▼
AI
   │
   │ Structured Data
   ▼
Validation
   │
   ▼
Lead Qualification
   │
   ├──────────────┐
   ▼              ▼
SQL            Google Sheets
   │
   ▼
Notification
   │
   ▼
Sales Team
```

---

# 13. Detailed Lead Processing Flow

Consider:

> "Hi, I'm looking for a 3-bedroom apartment around Lekki. My budget is around ₦80 million and I want to buy within two months."

The system processes it as follows:

### Step 1 — Customer

Customer sends message.

### Step 2 — React

React captures the message.

### Step 3 — FastAPI

FastAPI validates the request.

### Step 4 — n8n

FastAPI sends the request into the lead-processing workflow.

### Step 5 — AI

AI extracts structured information.

```json
{
  "property_type": "apartment",
  "bedrooms": 3,
  "location": "Lekki",
  "budget": 80000000,
  "transaction_type": "buy",
  "timeline": "within_3_months"
}
```

### Step 6 — Validation

The extracted data is checked.

### Step 7 — Qualification

The scoring rules are applied.

Example:

```text
Phone provided       +10
Budget provided      +20
Location provided    +15
Property type        +15
Buying soon          +25
Clear requirements   +15
-------------------------
Total                100
```

Lead:

```text
HOT
```

### Step 8 — Database

Lead is stored in SQL.

### Step 9 — Google Sheets

Lead information is synchronized.

### Step 10 — Notification

Sales team receives an alert.

### Step 11 — Customer Response

Customer receives a response.

---

# 14. Frontend Architecture

Recommended React structure:

```text
frontend/
│
├── src/
│   ├── components/
│   │   ├── ChatWindow.jsx
│   │   ├── MessageBubble.jsx
│   │   ├── MessageInput.jsx
│   │   └── LeadForm.jsx
│   │
│   ├── pages/
│   │   ├── ChatPage.jsx
│   │   └── DashboardPage.jsx
│   │
│   ├── services/
│   │   └── api.js
│   │
│   ├── hooks/
│   │
│   ├── utils/
│   │
│   ├── App.jsx
│   └── main.jsx
│
├── package.json
└── README.md
```

The exact structure can evolve during implementation.

---

# 15. Backend Architecture

Recommended FastAPI structure:

```text
backend/
│
├── app/
│   ├── main.py
│   │
│   ├── routes/
│   │   ├── chat.py
│   │   ├── leads.py
│   │   └── health.py
│   │
│   ├── models/
│   │   ├── lead.py
│   │   ├── customer.py
│   │   └── conversation.py
│   │
│   ├── schemas/
│   │   ├── lead.py
│   │   ├── chat.py
│   │   └── response.py
│   │
│   ├── services/
│   │   ├── lead_service.py
│   │   ├── scoring_service.py
│   │   ├── n8n_service.py
│   │   └── ai_service.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   └── session.py
│   │
│   └── config.py
│
├── tests/
│
├── requirements.txt
└── README.md
```

---

# 16. n8n Workflow Architecture

Rather than creating one enormous workflow, the system should use smaller workflows with clear responsibilities.

Recommended workflows:

```text
WF-01 — Receive Chat
WF-02 — Process Lead
WF-03 — AI Extraction
WF-04 — Lead Qualification
WF-05 — Store Lead
WF-06 — Google Sheets Sync
WF-07 — Sales Notification
WF-08 — Follow-Up
WF-09 — Error Handling
```

Some workflows may eventually be combined where separation provides no practical benefit.

---

# 17. WF-01 — Receive Chat

Purpose:

Receive customer messages.

Flow:

```text
Webhook
   ↓
Validate Request
   ↓
Create/Find Conversation
   ↓
Trigger Lead Processing
```

Input example:

```json
{
  "conversation_id": "conv_123",
  "message": "I need a 3-bedroom apartment in Lekki."
}
```

---

# 18. WF-02 — Process Lead

Purpose:

Coordinate the primary lead-processing pipeline.

Flow:

```text
Receive Message
      ↓
Get Conversation Context
      ↓
AI Extraction
      ↓
Validate Structured Data
      ↓
Check Missing Information
      ↓
IF Missing Information
      │
      ├── Yes → Generate Question
      │
      └── No → Qualification
                     ↓
                  Scoring
                     ↓
                  Storage
                     ↓
                Notification
```

---

# 19. WF-03 — AI Extraction

The AI workflow should transform natural language into structured information.

Input:

```text
"I need a 3 bedroom apartment around Lekki.
My budget is 80 million and I want to move in
within two months."
```

Output:

```json
{
  "property_type": "apartment",
  "bedrooms": 3,
  "location": "Lekki",
  "budget": 80000000,
  "transaction_type": "buy",
  "timeline": "within_3_months",
  "confidence": 0.94
}
```

The confidence field is optional but useful for future improvements.

---

# 20. AI Output Validation

AI output must not be trusted blindly.

The system should validate:

- Data types.
- Allowed enum values.
- Budget format.
- Bedroom values.
- Required structure.
- Unexpected fields.

Example:

```text
AI Output
   ↓
JSON Validation
   ↓
Business Validation
   ↓
Accepted / Rejected
```

If invalid:

```text
AI Output Invalid
       ↓
Retry / Fallback
       ↓
Human Escalation if necessary
```

---

# 21. Lead Qualification Architecture

Qualification should be deterministic where possible.

```text
Structured Lead
      ↓
Business Rules
      ↓
Score
      ↓
Classification
```

Example:

```python
score = 0

if phone:
    score += 10

if budget:
    score += 20

if location:
    score += 15

if property_type:
    score += 15

if buying_soon:
    score += 25

if clear_requirements:
    score += 15
```

Then:

```text
80–100 → HOT
50–79  → WARM
0–49   → COLD
```

The scoring logic may eventually be moved into FastAPI if it becomes sufficiently complex.

---

# 22. Conversation Management

Each customer conversation should have a unique identifier.

Example:

```text
conversation_id:
conv_8f31a
```

Messages should be associated with the conversation.

Example:

```text
Conversation
    │
    ├── Message 1
    ├── Message 2
    ├── Message 3
    └── Message 4
```

This allows the AI and system to understand previous context.

---

# 23. Data Flow for Missing Information

Example:

Customer:

> "I want to buy a house."

AI extracts:

```json
{
  "transaction_type": "buy",
  "property_type": "house"
}
```

Required information is missing.

The system checks:

```text
Location      ❌
Budget        ❌
Bedrooms      ❌
Timeline      ❌
```

Instead of creating a fully qualified lead, the bot responds:

> "I'd be happy to help. Which location are you interested in, and what is your approximate budget?"

The conversation continues until sufficient information is available.

---

# 24. API Architecture

The initial API should expose clear boundaries.

## POST /api/chat

Used to send customer messages.

Example request:

```json
{
  "conversation_id": "conv_123",
  "message": "I need a 3-bedroom apartment in Lekki."
}
```

Example response:

```json
{
  "conversation_id": "conv_123",
  "message": "What is your approximate budget?",
  "status": "collecting_information"
}
```

---

## POST /api/leads

Creates a lead where required.

---

## GET /api/leads

Returns leads for authorized internal users.

---

## GET /api/leads/{lead_id}

Returns a specific lead.

---

## PATCH /api/leads/{lead_id}

Updates lead information/status.

---

## POST /api/leads/{lead_id}/follow-up

Records or creates a follow-up action.

---

## GET /api/health

Used for health checks.

Example:

```json
{
  "status": "ok"
}
```

The final API contract will be defined separately in the API Specification document.

---

# 25. Database Architecture

The initial relational model should include the following major entities:

```text
Customer
   │
   └── Conversation
           │
           └── Messages

Customer
   │
   └── Lead
          │
          ├── Requirements
          ├── Qualification
          ├── Assignment
          ├── Status History
          └── Follow-Ups
```

---

# 26. Core Database Entities

## Customers

Stores customer information.

Possible fields:

```text
id
name
email
phone
created_at
updated_at
```

---

## Leads

Stores the primary sales opportunity.

Possible fields:

```text
id
customer_id
property_type
bedrooms
location
budget
transaction_type
timeline
intent
score
temperature
status
assigned_to
created_at
updated_at
```

---

## Conversations

Stores customer conversations.

Possible fields:

```text
id
customer_id
lead_id
session_id
created_at
updated_at
```

---

## Messages

Stores individual messages.

Possible fields:

```text
id
conversation_id
sender_type
content
created_at
```

Where:

```text
sender_type:
customer
bot
sales_rep
```

---

## Follow-Ups

Stores sales follow-up activity.

Possible fields:

```text
id
lead_id
sales_rep_id
notes
follow_up_date
status
created_at
```

---

# 27. SQL as System of Record

The architecture explicitly defines:

```text
SQL = Authoritative Application Database
```

Google Sheets is not the primary source of truth.

This prevents a situation where:

```text
SQL says:
Status = CONTACTED

Google Sheets says:
Status = NEW
```

The synchronization policy must define which system wins.

For the MVP:

```text
Application changes
       ↓
SQL
       ↓
Google Sheets
```

---

# 28. Google Sheets Synchronization

A basic synchronization workflow:

```text
Lead Created/Updated
        ↓
n8n
        ↓
Prepare Row
        ↓
Google Sheets
        ↓
Insert/Update Row
```

Recommended spreadsheet columns:

```text
Lead ID
Customer Name
Email
Phone
Property Type
Bedrooms
Location
Budget
Transaction Type
Timeline
Score
Temperature
Status
Assigned Sales Rep
Created At
Updated At
```

---

# 29. Sales Notification Flow

When a lead reaches a defined priority:

```text
Lead Qualified
      ↓
Score
      ↓
IF HOT
      ↓
Sales Notification
```

Normal leads may follow a less urgent notification process.

Example:

```text
HOT
→ Immediate notification

WARM
→ Standard notification

COLD
→ Store + normal follow-up
```

The exact notification channel will be determined by client requirements.

---

# 30. Lead Status Architecture

The initial state machine:

```text
NEW
 ↓
QUALIFIED
 ↓
ASSIGNED
 ↓
CONTACTED
 ↓
FOLLOW_UP
 ↓
NEGOTIATION
 ↓
CONVERTED
```

Alternative paths:

```text
NEW → UNQUALIFIED
CONTACTED → LOST
FOLLOW_UP → LOST
NEGOTIATION → LOST
```

The backend should prevent invalid status transitions where practical.

---

# 31. Error Handling Architecture

Errors should be handled at multiple layers.

```text
React
 ↓
FastAPI
 ↓
n8n
 ↓
AI / DB / External APIs
```

Each layer should handle failures appropriate to its responsibility.

---

# 32. Frontend Error Handling

Examples:

- Network unavailable.
- API timeout.
- Server error.
- Invalid request.

The customer should see a friendly message.

Example:

> "We're having trouble processing your request right now. Please try again."

Technical error details should not be exposed to the customer.

---

# 33. Backend Error Handling

FastAPI should:

- Validate requests.
- Return appropriate HTTP status codes.
- Log unexpected failures.
- Avoid exposing internal implementation details.

Example:

```text
400 → Invalid request
401 → Unauthorized
403 → Forbidden
404 → Resource not found
422 → Validation error
500 → Internal server error
```

---

# 34. n8n Error Handling

n8n workflows should have explicit error handling.

Example:

```text
Workflow
   ↓
Operation
   ↓
Success ─────────→ Continue
   │
   └── Failure
          ↓
      Error Handler
          ↓
      Log Failure
          ↓
      Retry / Alert
```

A failed notification should not necessarily mean the lead itself has been lost.

---

# 35. AI Failure Handling

AI can fail in several ways:

- Invalid JSON.
- Missing fields.
- Incorrect interpretation.
- API timeout.
- API unavailable.
- Hallucinated values.

Therefore:

```text
AI
 ↓
Validate
 ↓
Valid?
 ├── YES → Continue
 └── NO → Retry / Fallback
```

AI should never be the only source of truth for critical business operations.

---

# 36. Security Architecture

Sensitive credentials should be stored outside source code.

Examples:

```text
DATABASE_URL
N8N_WEBHOOK_URL
AI_API_KEY
GOOGLE_SERVICE_ACCOUNT
```

These should be managed using environment variables or secure credential storage.

Never:

```python
API_KEY = "actual-secret-key"
```

inside committed application code.

---

# 37. Authentication

Internal sales functionality should require authentication.

Customer chat may not require a traditional user account for the MVP.

A possible architecture:

```text
Customer
→ Public Chat API

Sales Team
→ Authenticated Internal API
```

Authentication strategy can be finalized during implementation.

---

# 38. Authorization

Different users may have different permissions.

Example:

```text
Customer
→ Own conversation

Sales Representative
→ Assigned leads

Sales Manager
→ Team leads

Administrator
→ System configuration
```

The MVP may begin with a simplified authorization model and expand later.

---

# 39. Observability

The system should provide visibility into failures and important events.

Track:

```text
Request ID
Conversation ID
Lead ID
Workflow execution
AI processing
Database operation
Notification status
Error information
Timestamp
```

A useful identifier chain is:

```text
Request ID
    ↓
Conversation ID
    ↓
Lead ID
    ↓
n8n Execution ID
```

This makes debugging significantly easier.

---

# 40. Logging Strategy

Logs should answer:

- What happened?
- When did it happen?
- Which lead was affected?
- Which workflow was running?
- Did the operation succeed?
- If it failed, why?

Avoid logging sensitive information unnecessarily.

---

# 41. Deployment Architecture

A possible MVP deployment:

```text
                    INTERNET
                       │
                       ▼
               ┌──────────────┐
               │ React App    │
               └──────┬───────┘
                      │
                      ▼
               ┌──────────────┐
               │ FastAPI      │
               └──────┬───────┘
                      │
                      ▼
               ┌──────────────┐
               │ n8n          │
               └──────┬───────┘
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
        SQL          AI       Google Sheets
```

The exact hosting providers are intentionally left open at this stage.

---

# 42. Development Environment

Developers should be able to run the major components locally.

Example:

```text
React
localhost:5173

FastAPI
localhost:8000

n8n
localhost:5678

SQL
localhost:5432
```

The exact ports can be changed if required.

---

# 43. Environment Separation

The project should eventually have:

```text
Development
Testing
Production
```

Each environment should have separate:

- Credentials.
- Databases.
- API keys.
- n8n workflows/configuration where necessary.

---

# 44. Recommended Repository Structure

The overall project may use:

```text
real-estate-lead-bot/
│
├── frontend/
│
├── backend/
│
├── n8n/
│   └── workflows/
│
├── database/
│   ├── migrations/
│   └── seeds/
│
├── docs/
│
├── tests/
│
├── .env.example
├── .gitignore
└── README.md
```

---

# 45. Data Ownership

Each component has a clear ownership boundary.

| Data/Responsibility | Owner |
|---|---|
| UI state | React |
| API validation | FastAPI |
| Workflow state | n8n |
| AI interpretation | AI layer |
| Persistent lead data | SQL |
| Operational spreadsheet | Google Sheets |
| Sales activity | Backend/SQL |
| Customer conversation | SQL |

---

# 46. Important Architectural Decision

One of the most important decisions is:

> **n8n is the orchestration engine, not the entire backend.**

We should avoid building:

```text
One Giant n8n Workflow
```

containing every business rule, API operation, database operation, AI prompt, and customer interaction.

Instead:

```text
React
  ↓
FastAPI
  ↓
n8n
  ↓
Specialized Services
```

This keeps the system maintainable.

---

# 47. AI and Business Logic Boundary

Another critical architectural decision:

```text
AI
=
Interpretation
```

while:

```text
Application Logic
=
Decision Making
```

For example, AI may determine:

```text
timeline = "within_1_month"
```

The business logic determines:

```text
within_1_month → +25 points
```

This makes qualification predictable and testable.

---

# 48. Reliability Strategy

The system should prioritize preserving lead data.

Recommended ordering:

```text
Receive
 ↓
Validate
 ↓
Persist
 ↓
Process
 ↓
Notify
```

rather than:

```text
Receive
 ↓
Notify
 ↓
Maybe save later
```

If notification fails, the lead should still exist in the database.

---

# 49. Idempotency

The system should avoid creating duplicate leads when the same request is accidentally processed more than once.

Potential identifiers:

```text
request_id
conversation_id
message_id
lead_id
```

For example, if n8n retries a database operation, the same lead should not be inserted twice.

---

# 50. Scalability Strategy

The MVP does not require complex infrastructure.

However, the architecture should allow:

```text
100 leads/day
       ↓
1,000 leads/day
       ↓
10,000+ leads/day
```

without fundamentally changing the product architecture.

Potential future improvements include:

- Background job queues.
- Caching.
- Database indexing.
- Horizontal API scaling.
- Dedicated AI processing workers.
- Message queues.

These are not required for the initial MVP.

---

# 51. Testing Strategy

Testing should occur at multiple levels.

## Unit Testing

Test:

- Scoring.
- Validation.
- Business rules.
- Utility functions.

## API Testing

Test:

- Endpoints.
- Validation.
- Authentication.
- Error responses.

## Workflow Testing

Test:

- n8n execution.
- AI integration.
- Database operations.
- Notifications.

## Integration Testing

Test:

```text
React
 ↓
FastAPI
 ↓
n8n
 ↓
AI
 ↓
SQL
 ↓
Notification
```

## End-to-End Testing

Simulate a real customer from initial enquiry through sales follow-up.

---

# 52. Critical Test Cases

The system should be tested with:

### Complete enquiry

```text
3-bedroom apartment
Lekki
₦80M
Buy
2 months
```

### Minimal enquiry

```text
"I want a house."
```

### Rental enquiry

```text
"2-bedroom apartment in Ikeja for rent."
```

### Land enquiry

```text
"I need land in Ibadan below ₦20M."
```

### Invalid information

```text
"My budget is banana."
```

### AI failure

Simulate an unavailable AI API.

### Database failure

Simulate SQL unavailable.

### Notification failure

Simulate notification service unavailable.

### Duplicate request

Send the same request multiple times.

### Human escalation

```text
"I want to speak to an agent."
```

---

# 53. Technical Decision Summary

| Decision | Choice |
|---|---|
| Frontend | React |
| Backend | FastAPI / Python |
| Automation | n8n |
| AI | LLM API |
| Primary database | SQL |
| Operational data | Google Sheets |
| API communication | REST/HTTP |
| Workflow communication | Webhooks/API |
| Version control | Git |
| Architecture | Modular service-oriented MVP |

---

# 54. Architecture Summary

The final MVP architecture is:

```text
                         CUSTOMER
                            │
                            ▼
                  ┌──────────────────┐
                  │      REACT       │
                  │ Customer Chat UI │
                  └────────┬─────────┘
                           │
                           │ REST API
                           ▼
                  ┌──────────────────┐
                  │     FASTAPI      │
                  │ Backend / API    │
                  └────────┬─────────┘
                           │
                           │ Webhook/API
                           ▼
                  ┌──────────────────┐
                  │       n8n        │
                  │ Workflow Engine  │
                  └────────┬─────────┘
                           │
            ┌──────────────┼──────────────┐
            │              │              │
            ▼              ▼              ▼
      ┌──────────┐   ┌──────────┐  ┌──────────────┐
      │    AI    │   │   SQL    │  │ Integrations │
      │ Language │   │ Database │  │              │
      └──────────┘   └──────────┘  └──────┬───────┘
                                          │
                              ┌───────────┼───────────┐
                              │           │           │
                              ▼           ▼           ▼
                         Google Sheets  Email     WhatsApp
                                          │
                                          ▼
                                    SALES TEAM
```

---

# 55. Final Engineering Principle

The system should be built around one central principle:

> **Use the simplest technology that is appropriate for each responsibility.**

Therefore:

```text
React
→ Interface

FastAPI
→ Application/API

n8n
→ Automation

AI
→ Understanding

SQL
→ Truth / Persistence

Google Sheets
→ Operational visibility

Sales Team
→ Human decision and follow-up
```

The result should be a system that is understandable, testable, maintainable, and extensible rather than simply a collection of connected tools.