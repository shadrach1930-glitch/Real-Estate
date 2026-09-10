# PrimeHomes Realty Real Estate Lead Bot
## Database Design & Data Model Specification

**Document Version:** 1.0  
**Project:** PrimeHomes Realty Real Estate Lead Bot  
**Status:** Approved for Development  
**Primary Database:** PostgreSQL  
**Secondary Operational Store:** Google Sheets  
**Backend:** Python + FastAPI  
**Automation:** n8n  

---

## 1. Purpose

This document defines the database structure for the PrimeHomes Realty Real Estate Lead Bot.

The database will store:

- Customers
- Leads
- Conversations
- Messages
- Property requirements
- Lead qualification results
- Sales representatives
- Lead assignments
- Lead status history
- Follow-up activities
- System processing information

The database is the **authoritative system of record**.

Google Sheets will be used for operational visibility and selected automation tasks but will not replace the primary database.

---

# 2. Database Design Principles

The database will follow these principles:

### 2.1 Single Source of Truth

PostgreSQL is the authoritative source for lead and customer information.

Google Sheets should not contain information that conflicts with the database.

### 2.2 Data Integrity

Important fields must be validated before being stored.

Examples:

- Valid email format
- Valid phone format
- Budget must be numeric
- Lead status must use an approved value
- Property type must use an approved value

### 2.3 Traceability

Important actions should be traceable.

For example:

```text
Customer message
       ↓
Conversation
       ↓
Lead created
       ↓
AI extraction
       ↓
Qualification
       ↓
Sales assignment
       ↓
Follow-up
       ↓
Conversion
```

### 2.4 Idempotency

The system should prevent duplicate records when the same request is processed more than once.

Every incoming request should have a unique identifier where appropriate.

### 2.5 Separation of Concerns

Customer information, lead information, conversations and sales activities should not all be stored in one large table.

The database will use related tables instead.

---

# 3. High-Level Data Model

The conceptual relationship is:

```text
CUSTOMER
   │
   ├───────────────┐
   │               │
   ▼               ▼
CONVERSATION      LEAD
   │               │
   ▼               ├── PROPERTY REQUIREMENT
MESSAGES           │
                   ├── QUALIFICATION
                   │
                   ├── ASSIGNMENT
                   │
                   ├── STATUS HISTORY
                   │
                   └── FOLLOW-UPS
```

Sales representatives interact primarily with leads.

Customers may have multiple conversations and potentially multiple leads.

---

# 4. Entity List

The initial database will contain the following tables:

| Table | Purpose |
|---|---|
| `customers` | Stores customer information |
| `leads` | Stores individual sales opportunities |
| `property_requirements` | Stores the customer's property preferences |
| `conversations` | Stores chat sessions |
| `messages` | Stores individual messages |
| `lead_qualifications` | Stores scoring and qualification results |
| `sales_reps` | Stores sales team members |
| `lead_assignments` | Tracks which salesperson handles a lead |
| `lead_status_history` | Tracks changes to lead status |
| `follow_ups` | Tracks future sales activities |
| `ai_extractions` | Stores structured information extracted by AI |

---

# 5. Customers Table

## Table: `customers`

Stores the identity and contact information of a potential customer.

### Fields

| Column | Type | Required | Description |
|---|---|---:|---|
| `id` | UUID | Yes | Unique customer ID |
| `name` | VARCHAR(150) | No | Customer name |
| `email` | VARCHAR(255) | No | Customer email |
| `phone` | VARCHAR(30) | No | Customer phone number |
| `created_at` | TIMESTAMP | Yes | Creation timestamp |
| `updated_at` | TIMESTAMP | Yes | Last update timestamp |

### Example

```text
id: c7c7...
name: John Doe
email: john@example.com
phone: +2348012345678
```

### Rules

A customer does not necessarily need to provide all contact information immediately.

For example, a customer may initially say:

> "I'm looking for a 2-bedroom apartment in Ikeja."

The system can create the customer and progressively collect additional information.

---

# 6. Leads Table

## Table: `leads`

A lead represents a specific real-estate sales opportunity.

A customer can have more than one lead over time.

### Fields

| Column | Type | Required | Description |
|---|---|---:|---|
| `id` | UUID | Yes | Unique lead ID |
| `customer_id` | UUID | Yes | Related customer |
| `intent` | VARCHAR(50) | Yes | Customer's primary intent |
| `transaction_type` | VARCHAR(20) | No | Buy or rent |
| `status` | VARCHAR(30) | Yes | Current lead status |
| `score` | INTEGER | No | Qualification score |
| `temperature` | VARCHAR(20) | No | HOT, WARM or COLD |
| `source` | VARCHAR(50) | No | Lead source |
| `created_at` | TIMESTAMP | Yes | Creation time |
| `updated_at` | TIMESTAMP | Yes | Last update |

### Possible `intent` values

```text
BUY
RENT
SELL
LAND
PROPERTY_ENQUIRY
GENERAL_ENQUIRY
```

### Possible `transaction_type` values

```text
BUY
RENT
```

### Possible `status` values

```text
NEW
QUALIFIED
ASSIGNED
CONTACTED
FOLLOW_UP
NEGOTIATION
CONVERTED
UNQUALIFIED
LOST
CLOSED
```

### Possible `temperature` values

```text
HOT
WARM
COLD
```

---

# 7. Property Requirements Table

## Table: `property_requirements`

Stores what the customer is looking for.

This is separated from the lead table because property requirements may become more detailed over time.

### Fields

| Column | Type | Required | Description |
|---|---|---:|---|
| `id` | UUID | Yes | Requirement ID |
| `lead_id` | UUID | Yes | Related lead |
| `property_type` | VARCHAR(50) | No | Apartment, house, land etc. |
| `bedrooms` | INTEGER | No | Number of bedrooms |
| `location` | VARCHAR(150) | No | Preferred location |
| `budget_min` | NUMERIC(15,2) | No | Minimum budget |
| `budget_max` | NUMERIC(15,2) | No | Maximum budget |
| `currency` | VARCHAR(10) | Yes | Currency |
| `additional_requirements` | TEXT | No | Other preferences |
| `created_at` | TIMESTAMP | Yes | Creation time |
| `updated_at` | TIMESTAMP | Yes | Last update |

### Example

```text
property_type: Apartment
bedrooms: 3
location: Lekki
budget_min: 70000000
budget_max: 80000000
currency: NGN
additional_requirements: "Prefer gated estate and parking"
```

---

# 8. Conversations Table

## Table: `conversations`

A conversation represents a customer's interaction with the bot.

### Fields

| Column | Type | Required | Description |
|---|---|---:|---|
| `id` | UUID | Yes | Conversation ID |
| `customer_id` | UUID | Yes | Customer |
| `lead_id` | UUID | No | Associated lead |
| `session_id` | VARCHAR(100) | Yes | Chat session identifier |
| `channel` | VARCHAR(30) | Yes | Source channel |
| `created_at` | TIMESTAMP | Yes | Start time |
| `updated_at` | TIMESTAMP | Yes | Last activity |

### Possible channels

```text
WEB
WHATSAPP
INSTAGRAM
EMAIL
OTHER
```

The initial implementation may only use:

```text
WEB
```

The database should nevertheless support additional channels later.

---

# 9. Messages Table

## Table: `messages`

Stores every important message exchanged during a conversation.

### Fields

| Column | Type | Required | Description |
|---|---|---:|---|
| `id` | UUID | Yes | Message ID |
| `conversation_id` | UUID | Yes | Related conversation |
| `sender_type` | VARCHAR(30) | Yes | Customer, bot or sales rep |
| `content` | TEXT | Yes | Message content |
| `external_message_id` | VARCHAR(150) | No | ID from external platform |
| `created_at` | TIMESTAMP | Yes | Message time |

### Possible sender types

```text
CUSTOMER
BOT
SALES_REP
SYSTEM
```

### Example

```text
sender_type: CUSTOMER

content:
"Hi, I'm looking for a 3-bedroom apartment around Lekki.
My budget is around ₦80 million."
```

---

# 10. Lead Qualifications Table

## Table: `lead_qualifications`

Stores the result of the lead-scoring process.

### Fields

| Column | Type | Required | Description |
|---|---|---:|---|
| `id` | UUID | Yes | Qualification ID |
| `lead_id` | UUID | Yes | Related lead |
| `score` | INTEGER | Yes | Total score |
| `temperature` | VARCHAR(20) | Yes | HOT/WARM/COLD |
| `reason` | TEXT | No | Explanation of score |
| `qualified_at` | TIMESTAMP | Yes | Qualification time |

### Example

```text
score: 85
temperature: HOT

reason:
"Customer supplied budget, location, property type
and indicated they intend to purchase within two months."
```

The score should be calculated by backend/business logic, not blindly trusted from the AI.

---

# 11. Sales Representatives Table

## Table: `sales_reps`

Stores members of the PrimeHomes sales team.

### Fields

| Column | Type | Required | Description |
|---|---|---:|---|
| `id` | UUID | Yes | Sales representative ID |
| `name` | VARCHAR(150) | Yes | Representative name |
| `email` | VARCHAR(255) | Yes | Work email |
| `phone` | VARCHAR(30) | No | Phone number |
| `is_active` | BOOLEAN | Yes | Whether currently active |
| `created_at` | TIMESTAMP | Yes | Creation time |

---

# 12. Lead Assignments Table

## Table: `lead_assignments`

Tracks which sales representative is responsible for a lead.

This should be a separate table rather than simply storing one salesperson ID on the lead because assignment can change.

### Fields

| Column | Type | Required | Description |
|---|---|---:|---|
| `id` | UUID | Yes | Assignment ID |
| `lead_id` | UUID | Yes | Lead |
| `sales_rep_id` | UUID | Yes | Assigned salesperson |
| `assigned_at` | TIMESTAMP | Yes | Assignment time |
| `unassigned_at` | TIMESTAMP | No | End of assignment |
| `reason` | VARCHAR(255) | No | Assignment reason |

### Example

```text
Lead #123
    ↓
Assigned to Sarah
    ↓
Sarah unavailable
    ↓
Reassigned to David
```

Both assignments remain in the history.

---

# 13. Lead Status History

## Table: `lead_status_history`

Stores every status change.

### Fields

| Column | Type | Required | Description |
|---|---|---:|---|
| `id` | UUID | Yes | History ID |
| `lead_id` | UUID | Yes | Lead |
| `old_status` | VARCHAR(30) | No | Previous status |
| `new_status` | VARCHAR(30) | Yes | New status |
| `changed_by` | VARCHAR(50) | Yes | Actor |
| `reason` | TEXT | No | Reason for change |
| `created_at` | TIMESTAMP | Yes | Change time |

### Example

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

This creates an audit trail for the lead lifecycle.

---

# 14. Follow-Ups Table

## Table: `follow_ups`

Stores tasks that sales representatives need to perform.

### Fields

| Column | Type | Required | Description |
|---|---|---:|---|
| `id` | UUID | Yes | Follow-up ID |
| `lead_id` | UUID | Yes | Related lead |
| `sales_rep_id` | UUID | No | Assigned salesperson |
| `follow_up_date` | TIMESTAMP | Yes | When follow-up should occur |
| `notes` | TEXT | No | Follow-up notes |
| `status` | VARCHAR(30) | Yes | Pending/completed/cancelled |
| `completed_at` | TIMESTAMP | No | Completion time |
| `created_at` | TIMESTAMP | Yes | Creation time |

### Possible statuses

```text
PENDING
COMPLETED
CANCELLED
OVERDUE
```

---

# 15. AI Extractions Table

## Table: `ai_extractions`

Stores structured information extracted from customer messages by the AI.

This table is useful for debugging, auditing and improving the AI workflow.

### Fields

| Column | Type | Required | Description |
|---|---|---:|---|
| `id` | UUID | Yes | Extraction ID |
| `lead_id` | UUID | No | Associated lead |
| `message_id` | UUID | Yes | Source message |
| `model` | VARCHAR(100) | Yes | AI model used |
| `extracted_data` | JSONB | Yes | Structured extraction |
| `confidence` | NUMERIC(5,2) | No | Confidence value |
| `created_at` | TIMESTAMP | Yes | Extraction time |

### Example JSON

```json
{
  "intent": "BUY",
  "property_type": "APARTMENT",
  "bedrooms": 3,
  "location": "Lekki",
  "budget": 80000000,
  "currency": "NGN",
  "timeline": "WITHIN_2_MONTHS"
}
```

The AI extraction is not automatically considered the final truth.

The backend validates the extracted information before updating the lead.

---

# 16. Relationships

## Customer → Conversations

One customer can have multiple conversations.

```text
Customer 1 ──────── * Conversations
```

## Customer → Leads

One customer can have multiple leads.

```text
Customer 1 ──────── * Leads
```

## Conversation → Messages

One conversation can contain many messages.

```text
Conversation 1 ──────── * Messages
```

## Lead → Property Requirements

Initially, a lead will normally have one active requirement set.

```text
Lead 1 ──────── 1 Property Requirement
```

The design can later support multiple requirement versions.

## Lead → Qualification

A lead may have multiple qualification records if it is re-qualified.

```text
Lead 1 ──────── * Qualifications
```

## Lead → Assignments

A lead may have multiple assignments throughout its lifecycle.

```text
Lead 1 ──────── * Assignments
```

## Lead → Status History

Every status change creates a history record.

```text
Lead 1 ──────── * Status History
```

## Lead → Follow-Ups

A lead can have multiple follow-up activities.

```text
Lead 1 ──────── * Follow-Ups
```

---

# 17. Foreign Key Structure

The main foreign keys are:

```text
customers.id
    ↓
conversations.customer_id

customers.id
    ↓
leads.customer_id

conversations.id
    ↓
messages.conversation_id

leads.id
    ↓
property_requirements.lead_id

leads.id
    ↓
lead_qualifications.lead_id

leads.id
    ↓
lead_assignments.lead_id

sales_reps.id
    ↓
lead_assignments.sales_rep_id

leads.id
    ↓
lead_status_history.lead_id

leads.id
    ↓
follow_ups.lead_id

sales_reps.id
    ↓
follow_ups.sales_rep_id

messages.id
    ↓
ai_extractions.message_id
```

---

# 18. Lead Scoring Model

The database stores the result of qualification but the scoring calculation belongs to application/business logic.

Initial scoring model:

| Criteria | Points |
|---|---:|
| Phone provided | +10 |
| Budget provided | +20 |
| Location provided | +15 |
| Property type provided | +15 |
| Buying soon | +25 |
| Clear requirements | +15 |

Maximum:

```text
100 points
```

### Classification

```text
80–100 → HOT
50–79  → WARM
0–49   → COLD
```

The scoring service in FastAPI should calculate this.

n8n can trigger the qualification workflow, but it should not become the sole owner of the business scoring rules.

---

# 19. Lead Timeline / Auditability

For every lead, the system should be able to reconstruct:

```text
When was the lead created?
        ↓
What did the customer initially say?
        ↓
What information did AI extract?
        ↓
What information was validated?
        ↓
What was the qualification score?
        ↓
Who was assigned?
        ↓
When did the status change?
        ↓
What follow-ups happened?
        ↓
Was the lead converted or lost?
```

This is important for debugging, sales management and future analytics.

---

# 20. Indexing Strategy

Indexes should be created on frequently searched fields.

Recommended indexes:

```text
customers.email
customers.phone

leads.customer_id
leads.status
leads.temperature
leads.created_at
leads.assigned_to / assignment relationship

conversations.customer_id
conversations.session_id

messages.conversation_id
messages.created_at

follow_ups.follow_up_date
follow_ups.status
```

This will improve performance as the number of leads grows.

---

# 21. Unique Constraints

Recommended unique constraints include:

```text
customers.email
```

where appropriate, although a customer may initially have no email.

For conversations:

```text
session_id
```

should be unique where the application guarantees globally unique sessions.

For external integrations:

```text
external_message_id
```

should be unique when provided.

This helps prevent duplicate messages.

---

# 22. Nullability Strategy

The system should not force the customer to provide every piece of information immediately.

For example:

```text
Name: Unknown
Email: Unknown
Phone: Unknown
Property: Apartment
Bedrooms: 2
Location: Ikeja
Budget: Unknown
Timeline: Unknown
```

The AI and automation workflow should identify missing information and ask targeted questions.

Example:

> "Thanks. What budget range are you working with?"

After the customer responds, the lead record is updated.

---

# 23. Data Lifecycle

The expected lifecycle is:

```text
Customer sends message
        ↓
Create/find customer
        ↓
Create/find conversation
        ↓
Store message
        ↓
AI extracts information
        ↓
Validate extracted information
        ↓
Create/update lead
        ↓
Create/update property requirements
        ↓
Calculate qualification
        ↓
Assign sales representative
        ↓
Update lead status
        ↓
Notify sales team
        ↓
Store follow-up activity
```

---

# 24. Google Sheets Synchronization

Google Sheets is an operational view of selected lead information.

Recommended columns:

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

The database remains authoritative.

Example:

```text
PostgreSQL
     │
     │ synchronization
     ▼
Google Sheets
```

If a conflict occurs:

```text
PostgreSQL wins.
```

---

# 25. Data Validation

Validation should happen at multiple levels.

### Frontend

Basic validation for user experience.

### FastAPI

Authoritative API validation.

### Database

Final integrity constraints.

### AI

Structured extraction validation.

### Business Logic

Qualification and workflow validation.

Therefore:

```text
AI says it found budget = "₦80 million"
             ↓
Backend validates
             ↓
Convert to numeric representation
             ↓
Store 80000000
```

---

# 26. Security Requirements

Customer information must be protected.

The application should:

- Use environment variables for database credentials.
- Never expose database credentials to React.
- Restrict direct database access.
- Validate API input.
- Use HTTPS in production.
- Avoid logging unnecessary customer information.
- Protect internal endpoints.
- Use role-based access when the sales dashboard is introduced.
- Encrypt sensitive data where appropriate.
- Use secure database credentials.
- Back up the database regularly.

---

# 27. Database Backup Strategy

Production should have automated backups.

Minimum strategy:

```text
Daily backup
+
Periodic backup verification
+
Recovery testing
```

A backup is only useful if it can actually be restored.

---

# 28. Example Complete Lead

Customer message:

> "Hi, I'm looking for a 3-bedroom apartment around Lekki. My budget is around ₦80 million and I'd like to buy within two months."

The database could contain:

### Customer

```text
name: Unknown
email: Unknown
phone: Unknown
```

### Lead

```text
intent: BUY
transaction_type: BUY
status: QUALIFIED
score: 90
temperature: HOT
```

### Property Requirement

```text
property_type: APARTMENT
bedrooms: 3
location: Lekki
budget_max: 80000000
currency: NGN
```

### Qualification

```text
score: 90
temperature: HOT
```

### Conversation

```text
channel: WEB
```

### Message

```text
sender_type: CUSTOMER
content: Original customer message
```

This gives the sales team a structured lead rather than an unstructured chat message.

---

# 29. Database Ownership

Each component has a clear responsibility.

| Component | Responsibility |
|---|---|
| React | Collect/display information |
| FastAPI | Validate requests and execute business logic |
| AI | Interpret natural language |
| n8n | Orchestrate workflows/integrations |
| PostgreSQL | Store authoritative data |
| Google Sheets | Operational visibility |
| Sales Team | Handle qualified opportunities |

The architecture should avoid allowing multiple components to independently modify the same business rules.

---

# 30. Final Data Model

The initial production-ready model is:

```text
                    ┌─────────────────┐
                    │    CUSTOMERS    │
                    └────────┬────────┘
                             │
                 ┌───────────┴───────────┐
                 │                       │
                 ▼                       ▼
        ┌────────────────┐      ┌────────────────┐
        │ CONVERSATIONS  │      │     LEADS      │
        └───────┬────────┘      └───────┬────────┘
                │                       │
                ▼             ┌─────────┼─────────┐
        ┌────────────────┐    │         │         │
        │    MESSAGES    │    ▼         ▼         ▼
        └───────┬────────┘ PROPERTY  QUALIFICATION
                │          REQUIREMENTS
                ▼
        ┌────────────────┐
        │ AI EXTRACTIONS │
        └────────────────┘

LEADS
  │
  ├── LEAD ASSIGNMENTS ─── SALES REPS
  │
  ├── STATUS HISTORY
  │
  └── FOLLOW UPS ───────── SALES REPS
```

---

# 31. Definition of Done

The database design is considered ready for implementation when:

- All core entities are defined.
- Relationships are defined.
- Primary keys are defined.
- Foreign keys are defined.
- Required fields are identified.
- Status values are defined.
- Lead scoring storage is defined.
- AI extraction storage is defined.
- Audit history is defined.
- Follow-up tracking is defined.
- Google Sheets synchronization fields are defined.
- Security considerations are documented.
- Indexing requirements are documented.
- PostgreSQL can be used as the authoritative source of truth.

---

# 32. Implementation Recommendation

The next implementation step should **not** be writing application code yet.

The recommended sequence is:

```text
PRD
  ↓
System Architecture
  ↓
Data Flow & Workflow Specification
  ↓
Database Design
  ↓
API Specification
  ↓
UI/UX Specification
  ↓
n8n Workflow Specification
  ↓
AI Specification
  ↓
Testing Strategy
  ↓
Development
```

The database design above becomes the foundation for the FastAPI models, Pydantic schemas, SQL migrations and eventually the React dashboard data structures.