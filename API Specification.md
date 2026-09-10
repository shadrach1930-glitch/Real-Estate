# PrimeHomes Realty Real Estate Lead Bot
## API Specification

**Document Version:** 1.0  
**Project:** PrimeHomes Realty Real Estate Lead Bot  
**Status:** Ready for Development  
**Backend:** Python + FastAPI  
**API Style:** REST  
**Primary Data Store:** PostgreSQL  
**Automation:** n8n  

---

# 1. Purpose

This document defines the API contract for the PrimeHomes Realty Real Estate Lead Bot.

The API acts as the controlled communication layer between:

```text
React Frontend
      ↓
   FastAPI
      ↓
PostgreSQL / n8n / AI Services
```

The API will handle:

- Customer conversations
- Lead creation
- Lead retrieval
- Lead updates
- Qualification
- Follow-ups
- Sales assignments
- Dashboard data
- Health checks
- n8n communication

---

# 2. API Design Principles

The API will follow these principles:

### 2.1 FastAPI Owns the Backend Contract

React should not communicate directly with PostgreSQL or n8n.

Instead:

```text
React → FastAPI → Database
```

or, where automation is required:

```text
React → FastAPI → n8n → Services
```

### 2.2 Validate Before Processing

Incoming data must be validated before business logic runs.

```text
Request
   ↓
Authentication
   ↓
Schema Validation
   ↓
Business Validation
   ↓
Processing
   ↓
Database
```

### 2.3 Consistent Responses

All endpoints should use predictable response structures.

### 2.4 No Business Logic in React

React should display information and collect input.

Lead scoring, status transitions and important validation should be controlled by the backend.

---

# 3. Base URL

Development:

```text
http://localhost:8000
```

API prefix:

```text
/api/v1
```

Therefore:

```text
http://localhost:8000/api/v1
```

Production will use HTTPS and a production domain.

---

# 4. API Endpoint Summary

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check API health |
| POST | `/chat` | Send customer message |
| GET | `/conversations/{id}` | Retrieve conversation |
| GET | `/leads` | List leads |
| POST | `/leads` | Create lead |
| GET | `/leads/{id}` | Retrieve lead |
| PATCH | `/leads/{id}` | Update lead |
| POST | `/leads/{id}/qualify` | Qualify lead |
| POST | `/leads/{id}/assign` | Assign sales representative |
| GET | `/leads/{id}/history` | Retrieve lead history |
| POST | `/leads/{id}/follow-ups` | Create follow-up |
| GET | `/leads/{id}/follow-ups` | Retrieve follow-ups |
| PATCH | `/follow-ups/{id}` | Update follow-up |
| POST | `/webhooks/n8n` | Receive n8n events |
| GET | `/dashboard/summary` | Dashboard metrics |

---

# 5. Health Check

## GET `/health`

Used to determine whether the API is running.

### Response

```json
{
  "status": "ok",
  "service": "primehomes-api"
}
```

### HTTP Status

```text
200 OK
```

This endpoint should not require authentication.

---

# 6. Send Customer Message

## POST `/api/v1/chat`

This is the primary endpoint used by the React chat interface.

### Request

```json
{
  "conversation_id": "uuid",
  "message": "I'm looking for a 3-bedroom apartment in Lekki",
  "customer": {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+2348012345678"
  }
}
```

The customer object can be partially populated.

For a new conversation:

```json
{
  "conversation_id": null,
  "message": "I want to buy a house in Lekki",
  "customer": {
    "name": "John Doe"
  }
}
```

---

# 7. Chat Processing Flow

When `/chat` receives a message:

```text
React
  ↓
POST /chat
  ↓
FastAPI validates request
  ↓
Find/Create Customer
  ↓
Find/Create Conversation
  ↓
Store Message
  ↓
Trigger Processing
  ↓
AI extracts information
  ↓
Validate extracted data
  ↓
Create/Update Lead
  ↓
Calculate qualification
  ↓
Trigger n8n
  ↓
Generate response
  ↓
Return response
```

---

# 8. Chat Response

### Example

```json
{
  "conversation_id": "conv-uuid",
  "message_id": "message-uuid",
  "lead_id": "lead-uuid",
  "reply": "Thanks. I can help with that. What is your budget range?",
  "lead_status": "NEW",
  "missing_information": [
    "budget"
  ]
}
```

The frontend only needs to render the `reply`.

---

# 9. Chat Response When Lead Is Qualified

Example:

```json
{
  "conversation_id": "conv-uuid",
  "message_id": "message-uuid",
  "lead_id": "lead-uuid",
  "reply": "Thanks. I have captured your requirements. A member of our sales team will follow up with you shortly.",
  "lead_status": "QUALIFIED",
  "lead_temperature": "HOT",
  "score": 90
}
```

---

# 10. Get Conversation

## GET `/api/v1/conversations/{conversation_id}`

Returns a conversation and its messages.

### Response

```json
{
  "id": "conversation-uuid",
  "customer_id": "customer-uuid",
  "lead_id": "lead-uuid",
  "channel": "WEB",
  "messages": [
    {
      "id": "message-1",
      "sender_type": "CUSTOMER",
      "content": "I'm looking for a 3-bedroom apartment.",
      "created_at": "2026-09-08T10:00:00Z"
    },
    {
      "id": "message-2",
      "sender_type": "BOT",
      "content": "What location are you interested in?",
      "created_at": "2026-09-08T10:00:03Z"
    }
  ]
}
```

---

# 11. Create Lead

## POST `/api/v1/leads`

This endpoint allows the backend or authorized internal system to create a lead directly.

### Request

```json
{
  "customer_id": "customer-uuid",
  "intent": "BUY",
  "transaction_type": "BUY",
  "property_requirements": {
    "property_type": "APARTMENT",
    "bedrooms": 3,
    "location": "Lekki",
    "budget_max": 80000000,
    "currency": "NGN"
  }
}
```

### Response

```json
{
  "id": "lead-uuid",
  "customer_id": "customer-uuid",
  "intent": "BUY",
  "transaction_type": "BUY",
  "status": "NEW",
  "score": 65,
  "temperature": "WARM",
  "created_at": "2026-09-08T10:00:00Z"
}
```

---

# 12. Get Lead

## GET `/api/v1/leads/{lead_id}`

Returns complete lead information.

### Response

```json
{
  "id": "lead-uuid",
  "customer": {
    "id": "customer-uuid",
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+2348012345678"
  },
  "intent": "BUY",
  "transaction_type": "BUY",
  "status": "QUALIFIED",
  "score": 90,
  "temperature": "HOT",
  "property_requirements": {
    "property_type": "APARTMENT",
    "bedrooms": 3,
    "location": "Lekki",
    "budget_max": 80000000,
    "currency": "NGN"
  },
  "assigned_sales_rep": {
    "id": "rep-uuid",
    "name": "Sarah"
  },
  "created_at": "2026-09-08T10:00:00Z",
  "updated_at": "2026-09-08T10:05:00Z"
}
```

---

# 13. List Leads

## GET `/api/v1/leads`

Used by the sales dashboard.

### Supported query parameters

```text
status
temperature
intent
assigned_to
page
limit
search
```

### Example

```text
GET /api/v1/leads?status=QUALIFIED&temperature=HOT
```

### Response

```json
{
  "items": [
    {
      "id": "lead-1",
      "customer_name": "John Doe",
      "property_type": "APARTMENT",
      "location": "Lekki",
      "budget": 80000000,
      "temperature": "HOT",
      "status": "QUALIFIED"
    }
  ],
  "page": 1,
  "limit": 20,
  "total": 1
}
```

---

# 14. Update Lead

## PATCH `/api/v1/leads/{lead_id}`

Used for controlled lead updates.

### Request

```json
{
  "status": "CONTACTED"
}
```

Or:

```json
{
  "status": "FOLLOW_UP",
  "notes": "Customer requested a callback tomorrow."
}
```

The backend must validate whether the requested status transition is allowed.

---

# 15. Lead Status Transitions

Valid lifecycle:

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

Alternative outcomes:

```text
NEW → UNQUALIFIED
QUALIFIED → LOST
CONTACTED → LOST
FOLLOW_UP → LOST
NEGOTIATION → LOST
```

The backend should reject invalid transitions.

For example:

```text
CONVERTED → NEW
```

should not normally be allowed.

---

# 16. Qualify Lead

## POST `/api/v1/leads/{lead_id}/qualify`

Triggers the qualification service.

### Request

No body required initially.

### Response

```json
{
  "lead_id": "lead-uuid",
  "score": 85,
  "temperature": "HOT",
  "reason": "Customer provided contact details, budget, location and a near-term purchase timeline."
}
```

---

# 17. Qualification Responsibility

The API should calculate the score using backend business rules.

```text
AI
 ↓
Extract information
 ↓
FastAPI
 ↓
Validate information
 ↓
Scoring Service
 ↓
Score
```

AI should not directly decide:

```text
"Score = 90"
```

without the backend verifying the underlying criteria.

---

# 18. Assign Sales Representative

## POST `/api/v1/leads/{lead_id}/assign`

### Request

```json
{
  "sales_rep_id": "sales-rep-uuid"
}
```

### Response

```json
{
  "lead_id": "lead-uuid",
  "sales_rep_id": "sales-rep-uuid",
  "status": "ASSIGNED",
  "assigned_at": "2026-09-08T10:10:00Z"
}
```

The assignment should also create a record in:

```text
lead_assignments
```

and a status-history record.

---

# 19. Lead History

## GET `/api/v1/leads/{lead_id}/history`

Returns important events related to the lead.

### Response

```json
{
  "lead_id": "lead-uuid",
  "events": [
    {
      "type": "STATUS_CHANGE",
      "old_status": "NEW",
      "new_status": "QUALIFIED",
      "created_at": "2026-09-08T10:05:00Z"
    },
    {
      "type": "ASSIGNMENT",
      "sales_rep": "Sarah",
      "created_at": "2026-09-08T10:07:00Z"
    }
  ]
}
```

This endpoint is particularly useful for the sales dashboard.

---

# 20. Create Follow-Up

## POST `/api/v1/leads/{lead_id}/follow-ups`

### Request

```json
{
  "sales_rep_id": "sales-rep-uuid",
  "follow_up_date": "2026-09-10T10:00:00Z",
  "notes": "Call customer and show available Lekki apartments."
}
```

### Response

```json
{
  "id": "follow-up-uuid",
  "lead_id": "lead-uuid",
  "status": "PENDING",
  "follow_up_date": "2026-09-10T10:00:00Z"
}
```

---

# 21. Get Follow-Ups

## GET `/api/v1/leads/{lead_id}/follow-ups`

### Response

```json
{
  "items": [
    {
      "id": "follow-up-uuid",
      "follow_up_date": "2026-09-10T10:00:00Z",
      "notes": "Call customer.",
      "status": "PENDING"
    }
  ]
}
```

---

# 22. Update Follow-Up

## PATCH `/api/v1/follow-ups/{follow_up_id}`

### Request

```json
{
  "status": "COMPLETED"
}
```

### Response

```json
{
  "id": "follow-up-uuid",
  "status": "COMPLETED",
  "completed_at": "2026-09-10T10:15:00Z"
}
```

---

# 23. n8n Webhook

## POST `/api/v1/webhooks/n8n`

This endpoint is used when n8n needs to send an event back to the backend.

### Example request

```json
{
  "event": "LEAD_PROCESSED",
  "lead_id": "lead-uuid",
  "status": "QUALIFIED",
  "score": 85
}
```

### Response

```json
{
  "received": true
}
```

This endpoint must be protected.

It should not be publicly writable without authentication or webhook verification.

---

# 24. n8n Integration Direction

The preferred architecture is:

```text
FastAPI
   │
   │ trigger
   ▼
 n8n
   │
   ├── AI
   ├── Google Sheets
   ├── Email
   ├── Notifications
   └── Other integrations
```

n8n can call internal FastAPI endpoints when required.

For example:

```text
n8n
 ↓
POST /api/v1/leads/{id}/qualify
```

---

# 25. Dashboard Summary

## GET `/api/v1/dashboard/summary`

Returns high-level metrics.

### Response

```json
{
  "total_leads": 250,
  "new_leads": 35,
  "hot_leads": 42,
  "warm_leads": 98,
  "cold_leads": 110,
  "qualified_leads": 140,
  "converted_leads": 25,
  "pending_follow_ups": 18
}
```

These figures should be calculated from PostgreSQL.

---

# 26. Error Response Standard

All API errors should follow a consistent format.

### Example

```json
{
  "error": {
    "code": "LEAD_NOT_FOUND",
    "message": "The requested lead does not exist.",
    "request_id": "req-12345"
  }
}
```

---

# 27. HTTP Status Codes

| Status | Meaning |
|---|---|
| `200` | Successful request |
| `201` | Resource created |
| `202` | Accepted for asynchronous processing |
| `400` | Invalid request |
| `401` | Unauthorized |
| `403` | Forbidden |
| `404` | Resource not found |
| `409` | Conflict |
| `422` | Validation error |
| `429` | Too many requests |
| `500` | Internal server error |
| `502` | External service failure |
| `503` | Service unavailable |

---

# 28. Validation Example

If a user submits:

```json
{
  "bedrooms": "three"
}
```

FastAPI should reject it rather than allowing invalid data into the database.

Example:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "bedrooms must be an integer.",
    "request_id": "req-123"
  }
}
```

---

# 29. Idempotency

Important operations should support idempotency.

For example, if the same customer message is accidentally submitted twice:

```text
Request A
Request A
```

the system should not create:

```text
Lead 1
Lead 2
```

for the same event.

An idempotency key can be supplied:

```text
Idempotency-Key: unique-request-id
```

The backend should store and check it for operations where duplicate processing could cause problems.

---

# 30. Authentication

Public customer endpoints and internal endpoints should eventually have different security requirements.

### Customer-facing

```text
POST /chat
```

may initially be accessible to the web application with rate limiting and appropriate abuse protection.

### Internal

Endpoints such as:

```text
/leads
/leads/{id}/assign
/dashboard/summary
/webhooks/n8n
```

should require authentication.

For the production dashboard, an authenticated user system should be implemented.

---

# 31. Rate Limiting

The chat endpoint should be protected from abuse.

Recommended:

```text
POST /chat
       ↓
Rate limiter
       ↓
Request processing
```

This becomes particularly important once the bot is publicly accessible.

---

# 32. API Request IDs

Every request should receive a unique request ID.

Example:

```text
X-Request-ID: 8f92e...
```

The request ID should appear in:

- API logs
- Error responses
- n8n processing logs
- Important database/system events

This allows a developer to trace:

```text
Frontend request
      ↓
FastAPI
      ↓
n8n
      ↓
AI
      ↓
Database
```

---

# 33. Asynchronous Processing

Not every operation needs to block the customer.

For example:

```text
Customer sends message
        ↓
FastAPI stores message
        ↓
FastAPI triggers processing
        ↓
AI/n8n processing
        ↓
Response
```

For longer operations, the API can return:

```text
202 Accepted
```

rather than keeping the HTTP request open unnecessarily.

For the first implementation, however, the chat flow can remain synchronous if response times are acceptable.

---

# 34. API Security Rules

The implementation must:

- Never expose database credentials.
- Never expose AI API keys to React.
- Never expose n8n credentials to the frontend.
- Validate all incoming data.
- Authenticate internal endpoints.
- Protect webhooks.
- Rate-limit public endpoints.
- Avoid sensitive information in logs.
- Use HTTPS in production.
- Restrict CORS to approved frontend origins.

---

# 35. CORS

During development:

```text
http://localhost:5173
```

may be allowed.

Production should only allow the actual frontend domain.

Example:

```text
Allowed Origins:
https://primehomes.example
```

Do not use:

```text
allow_origins=["*"]
```

in a production environment unless there is a specific, justified requirement.

---

# 36. FastAPI Project Structure

The API specification maps to the following backend structure:

```text
backend/
│
├── app/
│   ├── main.py
│   │
│   ├── routes/
│   │   ├── chat.py
│   │   ├── leads.py
│   │   ├── conversations.py
│   │   ├── followups.py
│   │   ├── dashboard.py
│   │   ├── webhooks.py
│   │   └── health.py
│   │
│   ├── schemas/
│   │   ├── chat.py
│   │   ├── lead.py
│   │   ├── customer.py
│   │   ├── followup.py
│   │   └── response.py
│   │
│   ├── services/
│   │   ├── lead_service.py
│   │   ├── scoring_service.py
│   │   ├── conversation_service.py
│   │   ├── n8n_service.py
│   │   └── ai_service.py
│   │
│   ├── models/
│   │   ├── customer.py
│   │   ├── lead.py
│   │   ├── conversation.py
│   │   ├── message.py
│   │   └── followup.py
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

# 37. API Documentation

FastAPI should automatically expose interactive documentation.

Development endpoints:

```text
/docs
/redoc
```

The OpenAPI schema should become the formal API contract between frontend and backend development.

---

# 38. Example End-to-End API Flow

Customer sends:

> "Hi, I'm looking for a 3-bedroom apartment in Lekki. My budget is ₦80 million."

### Step 1

React:

```text
POST /api/v1/chat
```

### Step 2

FastAPI validates request.

### Step 3

Message is stored.

### Step 4

AI extracts:

```json
{
  "intent": "BUY",
  "property_type": "APARTMENT",
  "bedrooms": 3,
  "location": "Lekki",
  "budget": 80000000
}
```

### Step 5

Backend validates extraction.

### Step 6

Lead is created/updated.

### Step 7

Qualification service calculates score.

### Step 8

n8n synchronizes the lead with Google Sheets.

### Step 9

n8n sends notification to the sales team if required.

### Step 10

FastAPI returns the response to React.

---

# 39. Important Architectural Rule

The API should not become a thin proxy for every system.

Each component has a defined responsibility:

```text
React
  = User Interface

FastAPI
  = Backend + API + Business Logic

n8n
  = Workflow Orchestration

AI
  = Language Understanding + Response Generation

PostgreSQL
  = Source of Truth

Google Sheets
  = Operational Visibility
```

This separation should remain throughout development.

---

# 40. Definition of Done

The API specification is considered complete when:

- All major endpoints are defined.
- Request schemas are defined.
- Response schemas are defined.
- Error responses are standardized.
- HTTP status codes are defined.
- Lead lifecycle rules are defined.
- Authentication requirements are identified.
- Webhook security is identified.
- Idempotency is defined.
- Rate limiting is identified.
- CORS requirements are defined.
- Request tracing is defined.
- FastAPI project structure is defined.
- React-to-FastAPI communication is defined.
- FastAPI-to-n8n communication is defined.
- Database ownership is clear.

---

# 41. Next Development Document

The next document should be:

## UI/UX Specification

It will define:

- Customer chat interface
- Sales dashboard
- Lead cards
- Lead details page
- Conversation interface
- Qualification indicators
- Follow-up interface
- Navigation
- Forms
- Loading states
- Empty states
- Error states
- Responsive behavior
- React component structure
- User flows

After the UI/UX document, we can define the **n8n Workflow Specification**, followed by the **AI/Prompt Specification**, and then move into actual development.