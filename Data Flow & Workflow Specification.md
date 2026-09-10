# DATA FLOW & WORKFLOW SPECIFICATION

## PrimeHomes Realty — Real Estate Lead Bot

**Document Version:** 1.0  
**Status:** Draft  
**Project Phase:** System Design  
**Depends On:** PRD v1.0, System Architecture v1.0  
**Date:** September 2026

---

# 1. Purpose

This document defines how data moves through the PrimeHomes Realty Real Estate Lead Bot.

It translates the system architecture into concrete workflows.

It defines:

- How a customer message enters the system.
- How React communicates with FastAPI.
- How FastAPI communicates with n8n.
- How n8n processes the message.
- How AI extracts structured information.
- How missing information is identified.
- How leads are qualified.
- How scores are calculated.
- How data is stored in SQL.
- How Google Sheets is synchronized.
- How sales notifications are triggered.
- How customer responses are returned.
- How follow-ups are handled.
- How failures are handled.

---

# 2. Core Data Flow

The primary system flow is:

```text
CUSTOMER
   ↓
REACT
   ↓
FASTAPI
   ↓
n8n
   ↓
CONVERSATION CONTEXT
   ↓
AI EXTRACTION
   ↓
VALIDATION
   ↓
MISSING INFORMATION CHECK
   ↓
LEAD QUALIFICATION
   ↓
LEAD SCORING
   ↓
SQL DATABASE
   ↓
GOOGLE SHEETS
   ↓
SALES NOTIFICATION
   ↓
CUSTOMER RESPONSE
```

Not every message will complete every step.

For example, an incomplete enquiry may stop at:

```text
AI Extraction
      ↓
Missing Information
      ↓
Customer Question
      ↓
Wait for Customer
```

---

# 3. System Actors

The system contains the following actors:

```text
Customer
React Frontend
FastAPI Backend
n8n
AI Service
SQL Database
Google Sheets
Notification Service
Sales Representative
Sales Manager
```

---

# 4. Data Flow Principles

The following principles apply throughout the system.

## Principle 1 — Validate Before Processing

Incoming data should be validated before being sent into deeper processing.

## Principle 2 — Persist Important Data

Important customer/lead information should be persisted rather than existing only inside an n8n execution.

## Principle 3 — AI Produces Structured Information

AI should convert natural language into structured data.

## Principle 4 — Business Rules Make Decisions

Lead scoring and other deterministic decisions should be handled through explicit business rules.

## Principle 5 — SQL Is the Source of Truth

SQL remains the authoritative application database.

## Principle 6 — Google Sheets Is a Secondary Operational Layer

Google Sheets should be synchronized from the primary system.

## Principle 7 — Failures Must Be Observable

A failed operation should be logged and identifiable.

---

# 5. Workflow Inventory

The MVP will use the following workflows.

| ID | Workflow | Purpose |
|---|---|---|
| WF-001 | Receive Chat | Receive customer messages |
| WF-002 | Process Conversation | Coordinate message processing |
| WF-003 | AI Extraction | Extract structured information |
| WF-004 | Validate Lead Data | Validate AI/system output |
| WF-005 | Collect Missing Information | Ask for missing requirements |
| WF-006 | Qualify Lead | Calculate lead priority |
| WF-007 | Store Lead | Persist lead information |
| WF-008 | Sync Google Sheets | Update operational spreadsheet |
| WF-009 | Notify Sales Team | Alert sales staff |
| WF-010 | Generate Response | Generate customer-facing response |
| WF-011 | Lead Follow-Up | Manage sales follow-up |
| WF-012 | Error Handling | Handle workflow failures |

---

# 6. WF-001 — Receive Chat

## Purpose

Receive messages from the React frontend through FastAPI.

The customer should never communicate directly with internal n8n credentials.

The flow is:

```text
Customer
   ↓
React
   ↓
FastAPI
   ↓
n8n
```

---

# 7. WF-001 Input

Example request:

```json
{
  "conversation_id": "conv_12345",
  "message": "I need a 3-bedroom apartment in Lekki."
}
```

Additional metadata may include:

```json
{
  "customer_id": "customer_123",
  "channel": "web",
  "timestamp": "2026-09-08T15:00:00Z"
}
```

---

# 8. WF-001 Processing

The workflow should:

1. Receive request.
2. Validate required fields.
3. Identify conversation.
4. Create conversation if it doesn't exist.
5. Store incoming message.
6. Trigger the processing workflow.
7. Return an appropriate response.

---

# 9. WF-001 Output

Example:

```json
{
  "conversation_id": "conv_12345",
  "status": "processing"
}
```

FastAPI can then manage how this result is presented to React.

---

# 10. WF-002 — Process Conversation

This is the central orchestration workflow.

Flow:

```text
Receive Message
       ↓
Load Conversation
       ↓
Load Existing Lead
       ↓
AI Extraction
       ↓
Validate Output
       ↓
Merge New Information
       ↓
Check Required Fields
       ↓
     Decision
      /     \
 Missing   Complete
    ↓          ↓
Ask Question  Qualify
               ↓
             Score
               ↓
             Store
               ↓
           Notification
```

---

# 11. Conversation Context

Before processing a new message, the system should retrieve relevant conversation information.

Example:

Previous conversation:

```text
Customer:
I need an apartment in Lekki.

Bot:
What's your budget?

Customer:
Around ₦80 million.
```

When the next message arrives, the system should know:

```text
location = Lekki
budget = 80,000,000
```

The AI should not treat each message as an isolated request.

---

# 12. Conversation Context Strategy

For the MVP, conversation context can be constructed from:

```text
Current message
+
Relevant previous messages
+
Existing structured lead information
```

Example:

```json
{
  "current_message": "I want to move in next month.",
  "existing_lead": {
    "location": "Lekki",
    "property_type": "apartment",
    "bedrooms": 3,
    "budget": 80000000
  }
}
```

AI can then extract:

```json
{
  "timeline": "within_1_month"
}
```

---

# 13. WF-003 — AI Extraction

## Purpose

Convert natural language into structured lead information.

Input:

```text
"I need something around Lekki. Three bedrooms would
be nice. My budget is around 80m and I want to move
within two months."
```

Output:

```json
{
  "intent": "buy",
  "property_type": "apartment",
  "bedrooms": 3,
  "location": "Lekki",
  "budget": 80000000,
  "transaction_type": "buy",
  "timeline": "within_3_months"
}
```

---

# 14. AI Extraction Rules

The AI should:

- Extract only information supported by the conversation.
- Preserve existing information.
- Update information when the customer corrects it.
- Return null/unknown when information is unavailable.
- Follow a strict schema.
- Avoid inventing property information.

Example:

Customer:

> "I'm looking for something around Ikeja."

Correct:

```json
{
  "location": "Ikeja"
}
```

Incorrect:

```json
{
  "location": "Ikeja",
  "budget": 50000000
}
```

The AI must not invent the budget.

---

# 15. Structured Lead Schema

The normalized AI output should resemble:

```json
{
  "customer": {
    "name": null,
    "email": null,
    "phone": null
  },
  "property": {
    "property_type": null,
    "bedrooms": null,
    "location": null,
    "budget": null
  },
  "transaction": {
    "type": null,
    "timeline": null
  },
  "intent": null
}
```

This provides a predictable contract between AI and the rest of the workflow.

---

# 16. WF-004 — Validate Lead Data

AI output should be validated before entering the business logic.

Validation should include:

### Type validation

```text
bedrooms → integer
budget → numeric
phone → valid string format
email → valid email format
```

### Enum validation

For example:

```text
transaction_type:
buy
rent
sell
```

### Range validation

Bedrooms should not reasonably be:

```text
-5
```

or:

```text
1000
```

without additional business validation.

---

# 17. Validation Flow

```text
AI Output
    ↓
Schema Validation
    ↓
Business Validation
    ↓
Valid?
 ┌──┴──┐
YES    NO
 ↓      ↓
Continue Retry/Fallback
```

---

# 18. WF-005 — Collect Missing Information

After extraction, the system determines whether enough information is available.

Example:

```text
Property Type ✓
Location ✓
Budget ✗
Bedrooms ✗
Timeline ✗
```

The system should identify the most useful next question.

Instead of:

> "Please provide your name, email, phone, budget, bedrooms, location, and timeline."

The bot should ask naturally:

> "What's your approximate budget, and how many bedrooms are you looking for?"

---

# 19. Progressive Information Collection

The bot should gather information progressively.

Example:

### Message 1

> "I want a house in Lekki."

Extracted:

```text
property_type = house
location = Lekki
```

Bot:

> "Great. What's your approximate budget?"

### Message 2

> "Around ₦80 million."

Extracted:

```text
budget = ₦80M
```

Bot:

> "How many bedrooms are you looking for?"

This produces a more natural conversation.

---

# 20. Required vs Optional Fields

Not every field needs to be mandatory.

Recommended classification:

### Core qualification fields

```text
Property type
Location
Transaction type
Budget
Timeline
```

### Customer contact fields

```text
Name
Phone
Email
```

### Additional information

```text
Bedrooms
Special requirements
Additional notes
```

The exact mandatory-field policy should be configurable.

---

# 21. WF-006 — Qualify Lead

Once enough information is available:

```text
Structured Lead
      ↓
Qualification Rules
      ↓
Score
      ↓
Temperature
```

---

# 22. Lead Scoring

Initial scoring:

| Condition | Points |
|---|---:|
| Phone provided | +10 |
| Budget provided | +20 |
| Location provided | +15 |
| Property type provided | +15 |
| Buying/renting soon | +25 |
| Clear requirements | +15 |

Maximum:

```text
100
```

---

# 23. Lead Temperature

The score is converted into:

```text
80–100 → HOT
50–79  → WARM
0–49   → COLD
```

Example:

```text
Score = 85

Temperature = HOT
```

---

# 24. Qualification Example

Customer:

> "I have ₦100 million and want a 4-bedroom apartment in Lekki this month."

Potential score:

```text
Budget               +20
Location             +15
Property type        +15
Bedrooms/requirements +15
Urgent timeline      +25
Phone                +10
-------------------------
TOTAL                100
```

Result:

```text
HOT
```

---

# 25. Qualification Should Be Deterministic

AI may extract:

```text
timeline = within_1_month
```

But the scoring engine determines:

```text
within_1_month = +25
```

This separation is intentional.

It allows us to modify the scoring system without changing the AI.

---

# 26. WF-007 — Store Lead

Once qualified, lead information is stored in SQL.

Flow:

```text
Qualified Lead
      ↓
Check Existing Lead
      ↓
Create / Update
      ↓
Save
      ↓
Return Lead ID
```

---

# 27. Create vs Update

If the customer is starting a new enquiry:

```text
Create Lead
```

If the customer is continuing an existing conversation:

```text
Update Lead
```

Example:

Existing:

```text
Budget = unknown
```

Customer later says:

> "My budget is ₦80 million."

System:

```text
UPDATE lead
SET budget = 80000000
```

It should not create a second lead simply because a new message arrived.

---

# 28. Lead Identification

The system should use identifiers such as:

```text
lead_id
customer_id
conversation_id
message_id
```

This helps prevent duplicate records.

---

# 29. WF-008 — Google Sheets Synchronization

After successful SQL persistence:

```text
SQL Lead Saved
      ↓
n8n
      ↓
Transform Data
      ↓
Google Sheets
```

The spreadsheet row should contain operational information.

Example:

```text
Lead ID
Name
Phone
Email
Property
Bedrooms
Location
Budget
Transaction
Timeline
Score
Temperature
Status
Assigned Rep
Created At
```

---

# 30. Google Sheets Sync Rules

Important rule:

> SQL is the primary source of truth.

Therefore:

```text
Application
   ↓
SQL
   ↓
Google Sheets
```

rather than:

```text
Application
 ↓
Google Sheets
 ↓
SQL
```

for normal lead creation.

---

# 31. Google Sheets Failure

If Google Sheets fails:

```text
SQL Save
   ↓
SUCCESS
   ↓
Google Sheets
   ↓
FAILURE
```

The lead should remain safely stored.

The system should:

1. Record the synchronization failure.
2. Retry where appropriate.
3. Alert administrators if necessary.
4. Avoid creating duplicate SQL leads.

---

# 32. WF-009 — Sales Notification

Notification is triggered after lead qualification/storage.

Flow:

```text
Lead Stored
    ↓
Check Temperature
    ↓
HOT?
 ┌──┴──┐
YES    NO
 ↓      ↓
Urgent  Standard
Alert   Notification
```

---

# 33. Hot Lead Notification

Example:

```text
NEW HOT LEAD

Lead ID: LH-1023

Customer:
John Doe

Phone:
080XXXXXXXX

Requirement:
4-bedroom apartment

Location:
Lekki

Budget:
₦100,000,000

Timeline:
Within 1 month

Score:
100

Priority:
HOT
```

---

# 34. Normal Lead Notification

Warm/cold leads can follow a less urgent notification strategy.

Example:

```text
New Lead

Customer: Jane Doe
Property: 2-bedroom apartment
Location: Ikeja
Budget: ₦50M
Score: 65
Priority: WARM
```

---

# 35. WF-010 — Generate Customer Response

The response workflow determines what the customer should receive.

There are three major response types.

### Type A — Missing information

```text
Ask a question.
```

### Type B — Information complete

```text
Acknowledge requirements.
```

### Type C — Human escalation

```text
Tell customer a sales representative will assist.
```

---

# 36. Customer Response Rules

The bot should be helpful but should not make unsupported claims.

It may say:

> "I've captured your requirements."

It should not say:

> "We have a 3-bedroom apartment available in Lekki for ₦80 million."

unless the system has verified that information.

---

# 37. Response Flow

```text
Processing Complete
       ↓
Determine Response Type
       ↓
 ┌─────┼──────────┐
 ↓     ↓          ↓
Ask   Acknowledge Escalate
 ↓     ↓          ↓
Customer Response
```

---

# 38. Returning the Response to React

The final response should travel back:

```text
n8n
 ↓
FastAPI
 ↓
React
 ↓
Customer
```

Example API response:

```json
{
  "conversation_id": "conv_12345",
  "message": "What is your approximate budget?",
  "status": "collecting_information"
}
```

---

# 39. End-to-End Sequence

The complete synchronous interaction is:

```text
Customer
   │
   │ Message
   ▼
React
   │
   │ POST /api/chat
   ▼
FastAPI
   │
   │
   ▼
n8n
   │
   ├── Load Context
   │
   ├── AI Extraction
   │
   ├── Validation
   │
   ├── Missing Info?
   │
   ├── Qualification
   │
   ├── Scoring
   │
   ├── SQL
   │
   ├── Google Sheets
   │
   ├── Notification
   │
   └── Response
   │
   ▼
FastAPI
   │
   ▼
React
   │
   ▼
Customer
```

---

# 40. Lead Lifecycle Flow

Once a lead exists, its lifecycle is:

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

Alternative:

```text
NEW → UNQUALIFIED

CONTACTED → LOST

FOLLOW_UP → LOST

NEGOTIATION → LOST
```

---

# 41. WF-011 — Lead Follow-Up

Sales follow-up is separate from the initial customer-processing workflow.

Example:

```text
Sales Rep receives lead
       ↓
Opens lead
       ↓
Contacts customer
       ↓
Updates status
       ↓
Adds notes
       ↓
Sets follow-up date
```

---

# 42. Follow-Up Data

A follow-up record may contain:

```json
{
  "lead_id": "lead_123",
  "sales_rep_id": "rep_456",
  "status": "follow_up",
  "notes": "Customer requested property viewing.",
  "next_follow_up": "2026-09-12T10:00:00"
}
```

---

# 43. Follow-Up Automation

Future automation can monitor upcoming follow-ups:

```text
Scheduled Check
      ↓
Find Due Follow-Ups
      ↓
Notify Sales Rep
```

Example:

> "Reminder: Follow up with John Doe regarding the 4-bedroom Lekki property enquiry."

---

# 44. WF-012 — Error Handling

All critical workflows should have error handling.

General pattern:

```text
Workflow
   ↓
Operation
   ↓
Success → Continue
   │
   └── Failure
          ↓
       Log Error
          ↓
       Retry?
        /    \
      YES     NO
       ↓       ↓
    Retry    Alert
```

---

# 45. Error Categories

## Category A — Validation Error

Example:

```text
Invalid email
Invalid budget
Missing message
```

Action:

```text
Return validation response.
```

---

## Category B — AI Error

Example:

```text
AI API unavailable.
```

Action:

```text
Retry
 ↓
Fallback
 ↓
Human escalation if necessary
```

---

## Category C — Database Error

Example:

```text
SQL unavailable.
```

Action:

```text
Retry
 ↓
Log
 ↓
Alert
```

Customer should not receive a false confirmation that their lead was saved.

---

## Category D — Integration Error

Example:

```text
Google Sheets unavailable.
```

Action:

```text
Lead remains in SQL.
 ↓
Retry synchronization.
```

---

# 46. Retry Strategy

Retries should be used carefully.

Recommended for temporary failures:

```text
Attempt 1
 ↓
Wait
 ↓
Attempt 2
 ↓
Wait
 ↓
Attempt 3
 ↓
Failure Handler
```

Not every error should be retried.

For example:

```text
Invalid customer input
```

should not be retried automatically.

---

# 47. Idempotency Strategy

Operations that create records should be idempotent.

Example:

If the same message is accidentally submitted twice:

```text
message_id = msg_123
```

The system should recognize that it has already processed the message.

This prevents:

```text
One message
   ↓
Two leads
```

---

# 48. Duplicate Lead Strategy

A duplicate lead may be detected using combinations of:

```text
customer phone
+
active conversation
```

or:

```text
conversation_id
```

The exact deduplication strategy will be finalized during database implementation.

---

# 49. Data Transformation

Data will move through several representations.

### Stage 1 — User Message

```text
"I need a 3 bedroom apartment in Lekki for 80m."
```

### Stage 2 — AI Structured Data

```json
{
  "property_type": "apartment",
  "bedrooms": 3,
  "location": "Lekki",
  "budget": 80000000
}
```

### Stage 3 — Qualified Lead

```json
{
  "score": 70,
  "temperature": "WARM"
}
```

### Stage 4 — Database Record

```text
lead_id = LEAD-001
score = 70
temperature = WARM
status = QUALIFIED
```

### Stage 5 — Sales Notification

Human-readable summary.

---

# 50. Data Ownership During Processing

| Data | Owner |
|---|---|
| Raw customer message | Conversation/SQL |
| Structured extraction | Processing layer |
| Lead score | Business logic |
| Lead status | Backend/database |
| Sales notes | Sales system/database |
| Spreadsheet view | Google Sheets |
| Workflow execution data | n8n |

---

# 51. Recommended n8n Node Pattern

A typical workflow may look like:

```text
Webhook
   ↓
Set / Edit Fields
   ↓
HTTP Request
   ↓
AI Model
   ↓
Structured Output Parser
   ↓
IF
   ↓
Code / Business Logic
   ↓
Postgres
   ↓
Google Sheets
   ↓
Notification
   ↓
Respond
```

The exact nodes will depend on the final implementation.

---

# 52. Where Code Nodes Should Be Used

Code should only be introduced where it adds value.

Good examples:

- Score calculation.
- Data transformation.
- Complex validation.
- Custom formatting.
- Special business rules.

Avoid using Code nodes for tasks that standard n8n nodes already handle effectively.

---

# 53. Where FastAPI Should Be Used

FastAPI should handle logic that belongs to the application/backend.

Examples:

- Complex reusable business logic.
- Database service operations.
- Authentication.
- Custom APIs.
- Advanced validation.
- Logic that must be shared by multiple clients.

---

# 54. Where n8n Should Be Used

n8n is best suited for:

- Connecting services.
- Triggering workflows.
- AI orchestration.
- Notifications.
- Google Sheets synchronization.
- Scheduled jobs.
- External APIs.
- Workflow branching.

---

# 55. Where SQL Should Be Used

SQL should store durable application data.

Examples:

```text
Customers
Leads
Conversations
Messages
Follow-ups
Assignments
Status history
```

---

# 56. Where Google Sheets Should Be Used

Google Sheets should provide:

```text
Operational visibility
Simple reporting
Manual sales-team access
n8n integration
```

It should not become the application's complex relational data layer.

---

# 57. Complete Example — High-Value Lead

Customer sends:

> "Hi, I'm looking for a 4-bedroom apartment in Lekki. My budget is ₦100 million and I want to buy this month."

### React

Sends:

```json
{
  "conversation_id": "conv_1001",
  "message": "Hi, I'm looking for a 4-bedroom apartment in Lekki. My budget is ₦100 million and I want to buy this month."
}
```

### FastAPI

Validates request.

### n8n

Receives message.

### AI

Returns:

```json
{
  "property_type": "apartment",
  "bedrooms": 4,
  "location": "Lekki",
  "budget": 100000000,
  "transaction_type": "buy",
  "timeline": "within_1_month"
}
```

### Qualification

Score:

```text
Budget             +20
Location           +15
Property Type      +15
Bedrooms/Details   +15
Urgent Timeline    +25
```

If phone is available:

```text
Phone              +10
```

Potential score:

```text
100
```

### SQL

Lead stored.

### Google Sheets

Lead synchronized.

### Notification

Sales team alerted.

### Response

Customer receives an acknowledgement.

---

# 58. Complete Example — Incomplete Lead

Customer:

> "Hello, I want to buy a house."

AI:

```json
{
  "property_type": "house",
  "transaction_type": "buy",
  "location": null,
  "budget": null,
  "bedrooms": null,
  "timeline": null
}
```

System detects missing information.

Bot:

> "I'd be happy to help. Which location are you interested in, and what is your approximate budget?"

No final qualification is performed yet.

---

# 59. Complete Example — Existing Lead Update

Customer initially says:

> "I need a 2-bedroom apartment in Ikeja."

Stored:

```text
Property = Apartment
Bedrooms = 2
Location = Ikeja
```

Later:

> "My budget is ₦3 million yearly and I need it next month."

System updates:

```text
Budget = ₦3,000,000
Transaction = Rent
Timeline = Within 1 month
```

The system should update the existing lead rather than creating a second lead.

---

# 60. Complete Example — Human Escalation

Customer:

> "I don't want to speak with a bot. Connect me to an agent."

AI/logic identifies:

```text
intent = human_escalation
```

Flow:

```text
Customer
 ↓
n8n
 ↓
Escalation
 ↓
Sales Notification
 ↓
Assign Sales Rep
 ↓
Customer informed
```

---

# 61. Workflow Dependency Map

The workflows depend on each other as follows:

```text
WF-001 Receive Chat
        ↓
WF-002 Process Conversation
        ↓
WF-003 AI Extraction
        ↓
WF-004 Validation
        ↓
WF-005 Missing Information
        │
        └───────────────┐
                        │
                        ▼
                 WF-006 Qualification
                        ↓
                 WF-007 Store Lead
                        ↓
                 ┌──────┴──────┐
                 ↓             ↓
          WF-008 Sheets   WF-009 Notification
                 │             │
                 └──────┬──────┘
                        ↓
                 WF-010 Response
```

WF-011 and WF-012 operate around the lifecycle.

---

# 62. Architectural Data Path

The fundamental data path is:

```text
RAW DATA
   ↓
VALIDATION
   ↓
AI INTERPRETATION
   ↓
STRUCTURED DATA
   ↓
BUSINESS LOGIC
   ↓
QUALIFIED DATA
   ↓
PERSISTENCE
   ↓
INTEGRATIONS
   ↓
HUMAN ACTION
```

---

# 63. Design Constraints

The following constraints apply:

1. AI should not be trusted as a database.
2. Google Sheets should not replace SQL.
3. n8n should not contain every business rule.
4. React should not contain secret credentials.
5. FastAPI should validate incoming requests.
6. Critical operations should be observable.
7. Lead creation should be idempotent.
8. Customer responses should not contain unsupported claims.
9. Important customer information should be persisted.
10. System failures should not silently lose leads.

---

# 64. Workflow Success Criteria

The workflow system is successful when:

```text
Customer Message
       ↓
Successfully Received
       ↓
Successfully Understood
       ↓
Successfully Structured
       ↓
Successfully Validated
       ↓
Successfully Qualified
       ↓
Successfully Stored
       ↓
Successfully Synchronized
       ↓
Successfully Notified
       ↓
Customer Receives Response
```

For incomplete enquiries:

```text
Customer Message
       ↓
Understand
       ↓
Identify Missing Information
       ↓
Ask Customer
       ↓
Continue Conversation
```

---

# 65. Final Workflow Architecture

The complete system can be summarized as:

```text
                         CUSTOMER
                            │
                            ▼
                    ┌───────────────┐
                    │ React Chat UI │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │    FastAPI    │
                    │ API / Backend │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │     n8n       │
                    │ Orchestration │
                    └───────┬───────┘
                            │
                            ▼
                   ┌────────────────┐
                   │ Conversation   │
                   │ Context        │
                   └───────┬────────┘
                           │
                           ▼
                   ┌────────────────┐
                   │      AI        │
                   │ Extraction     │
                   └───────┬────────┘
                           │
                           ▼
                   ┌────────────────┐
                   │   Validation   │
                   └───────┬────────┘
                           │
                    ┌──────┴──────┐
                    │             │
                 Missing       Complete
                    │             │
                    ▼             ▼
                 Ask User     Qualification
                                  │
                                  ▼
                              Lead Score
                                  │
                                  ▼
                              SQL Database
                                  │
                         ┌────────┴────────┐
                         ▼                 ▼
                  Google Sheets       Notification
                                           │
                                           ▼
                                      Sales Team
```

---

# 66. Final Engineering Rule

The most important rule for implementation is:

> **Every piece of data should have a clear owner, every workflow should have a clear responsibility, and every failure should have a defined recovery path.**

The system should therefore remain:

```text
React
→ Interface

FastAPI
→ API + Backend

n8n
→ Orchestration

AI
→ Understanding

SQL
→ Persistent Truth

Google Sheets
→ Operational View

Sales Team
→ Human Action
```

This separation should be preserved throughout development.