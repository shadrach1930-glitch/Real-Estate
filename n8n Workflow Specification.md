# PrimeHomes Realty Real Estate Lead Bot
## n8n Workflow Specification

**Document Version:** 1.0  
**Project:** PrimeHomes Realty Real Estate Lead Bot  
**Status:** Ready for Development  
**Automation Platform:** n8n  
**Backend:** Python + FastAPI  
**Database:** PostgreSQL  
**Operational Store:** Google Sheets  
**AI Layer:** LLM API  

---

# 1. Purpose

This document defines the automation workflows that will be implemented in n8n.

n8n is responsible for **orchestrating processes and integrations**.

It is not the primary database and should not contain the application's core business logic.

The overall architecture is:

```text
Customer
   ↓
React Chat
   ↓
FastAPI
   ↓
n8n
   ↓
┌───────────────┬────────────────┬─────────────────┐
│      AI       │   PostgreSQL   │ Notifications   │
└───────────────┴────────────────┴─────────────────┘
   ↓
Response
   ↓
Customer
```

---

# 2. n8n Responsibilities

n8n will handle:

- Workflow orchestration
- AI service calls
- Google Sheets synchronization
- Sales notifications
- Follow-up automation
- External integrations
- Scheduled jobs
- Error routing
- Workflow-level logging

FastAPI remains responsible for:

- API validation
- Database operations
- Business rules
- Lead scoring
- Authentication
- Core application logic

---

# 3. Workflow Inventory

The initial system will contain:

| ID | Workflow | Purpose |
|---|---|---|
| WF-001 | Receive Customer Message | Receive/process new chat events |
| WF-002 | Process Conversation | Prepare context for AI |
| WF-003 | AI Lead Extraction | Extract structured information |
| WF-004 | Validate Lead Data | Validate AI output |
| WF-005 | Collect Missing Information | Determine what to ask customer |
| WF-006 | Qualify Lead | Calculate/update qualification |
| WF-007 | Store Lead | Persist lead information |
| WF-008 | Google Sheets Sync | Update operational spreadsheet |
| WF-009 | Sales Notification | Notify sales team |
| WF-010 | Generate Customer Response | Generate response |
| WF-011 | Follow-Up Automation | Manage scheduled follow-ups |
| WF-012 | Error Handling | Handle failed workflows |

---

# 4. WF-001 — Receive Customer Message

## Purpose

Start the lead-processing pipeline when FastAPI receives a customer message.

### Trigger

n8n Webhook.

```text
POST /webhook/primehomes/chat
```

### Input

```json
{
  "request_id": "req-123",
  "conversation_id": "conv-123",
  "customer_id": "customer-123",
  "message_id": "message-123",
  "message": "I'm looking for a 3-bedroom apartment in Lekki."
}
```

### Workflow

```text
Webhook
   ↓
Validate Input
   ↓
Check Idempotency
   ↓
Get Conversation Context
   ↓
Process Conversation
```

---

# 5. WF-001 Node Structure

Recommended nodes:

```text
1. Webhook
2. Set / Normalize Input
3. IF — Required Fields Present?
4. HTTP Request — FastAPI
5. IF — Already Processed?
6. Execute Workflow — WF-002
```

The workflow should not proceed if critical identifiers are missing.

---

# 6. WF-002 — Process Conversation

## Purpose

Prepare the information required by the AI.

The AI should not receive only the latest message when context is important.

### Input

```text
Current message
+
Previous relevant messages
+
Existing structured lead data
```

### Example

Current message:

> "My budget is around 80 million."

Previous conversation:

> "I'm looking for a 3-bedroom apartment in Lekki."

The AI should understand that:

```text
budget = ₦80,000,000
```

belongs to the existing property enquiry.

---

# 7. Context Preparation

n8n requests conversation information from FastAPI.

```text
n8n
 ↓
GET /api/v1/conversations/{conversation_id}
```

The result is normalized into:

```json
{
  "customer": {
    "name": "John Doe",
    "phone": "+2348012345678"
  },
  "current_message": "My budget is around 80 million.",
  "previous_messages": [
    "I'm looking for a 3-bedroom apartment in Lekki."
  ],
  "existing_requirements": {
    "property_type": "APARTMENT",
    "bedrooms": 3,
    "location": "Lekki"
  }
}
```

Then:

```text
Execute Workflow
        ↓
WF-003
```

---

# 8. WF-003 — AI Lead Extraction

## Purpose

Convert natural language into structured data.

### Input

Customer conversation context.

### AI Output

The AI must return structured JSON.

Example:

```json
{
  "intent": "BUY",
  "transaction_type": "BUY",
  "property_type": "APARTMENT",
  "bedrooms": 3,
  "location": "Lekki",
  "budget_min": null,
  "budget_max": 80000000,
  "currency": "NGN",
  "timeline": "WITHIN_2_MONTHS",
  "contact": {
    "name": null,
    "email": null,
    "phone": null
  },
  "missing_information": [
    "name",
    "phone"
  ]
}
```

---

# 9. AI Output Rules

The AI must:

- Return valid structured JSON.
- Never invent customer information.
- Never invent property availability.
- Preserve previously confirmed information.
- Identify uncertain information.
- Identify missing information.
- Normalize obvious variations where safe.

For example:

```text
"80m"
"80 million"
"₦80,000,000"
```

can be interpreted as:

```text
80000000 NGN
```

when the context clearly indicates Nigerian naira.

---

# 10. AI Must Not Decide Business Rules

The AI can say:

```json
{
  "budget_max": 80000000
}
```

But it should not independently decide:

```json
{
  "temperature": "HOT"
}
```

The qualification service should determine that.

Therefore:

```text
AI
 ↓
Extract
 ↓
Backend validation
 ↓
Business rules
 ↓
Qualification
```

---

# 11. WF-004 — Validate Lead Data

The extracted AI response enters a validation stage.

```text
AI Output
   ↓
Parse JSON
   ↓
Validate Schema
   ↓
Validate Values
   ↓
Normalize Data
```

### Example validation

```text
bedrooms = 3
```

Valid.

```text
bedrooms = "three"
```

Invalid for the internal schema unless normalized first.

---

# 12. AI Failure

If AI returns malformed JSON:

```text
AI
 ↓
Invalid JSON
 ↓
Validation fails
 ↓
Retry
```

The workflow should have a limited retry strategy.

Example:

```text
Attempt 1
   ↓
Attempt 2
   ↓
If still failed
   ↓
Error workflow
```

Do not retry indefinitely.

---

# 13. Low-Confidence Extraction

If the AI cannot confidently determine something:

```text
location:
"Maybe Lekki or Ajah"
```

the system should not silently select one.

Instead:

```text
location = null
confidence = LOW
```

The bot can ask:

> "Would you prefer Lekki or Ajah?"

---

# 14. WF-005 — Collect Missing Information

After extraction and validation, the system determines what information is missing.

Example:

```json
{
  "property_type": "APARTMENT",
  "bedrooms": 3,
  "location": "Lekki",
  "budget_max": null,
  "phone": null
}
```

Missing:

```text
budget
phone
```

The bot should ask for the most useful missing information first.

---

# 15. Missing Information Priority

Suggested order:

```text
1. Intent
2. Transaction type
3. Property type
4. Location
5. Budget
6. Bedrooms
7. Timeline
8. Name
9. Phone
10. Email
```

This is not an absolute rule.

The workflow should avoid asking unnecessary questions.

For example, if the customer already gave:

```text
"I need a 3-bedroom apartment in Lekki for ₦80m."
```

the bot should not ask:

> "What type of property are you looking for?"

---

# 16. WF-006 — Qualify Lead

Once enough information exists, the lead is sent through the qualification process.

### Flow

```text
Validated Lead
      ↓
Scoring Service
      ↓
Calculate Score
      ↓
Determine Temperature
```

Example:

```text
Phone provided        +10
Budget provided       +20
Location provided     +15
Property type         +15
Buying soon           +25
Clear requirements    +15
--------------------------------
Total                 100
```

Classification:

```text
80–100 = HOT
50–79  = WARM
0–49   = COLD
```

---

# 17. WF-007 — Store Lead

The lead is persisted in PostgreSQL.

Preferred flow:

```text
Validate
   ↓
Create/Update Customer
   ↓
Create/Update Lead
   ↓
Create/Update Requirements
   ↓
Create Qualification
   ↓
Create Status History
```

n8n should use FastAPI for controlled database operations where practical.

---

# 18. Important Persistence Rule

Never notify sales before the lead is safely persisted.

Incorrect:

```text
Customer
 ↓
AI
 ↓
Notify Sales
 ↓
Database fails
```

Correct:

```text
Customer
 ↓
AI
 ↓
Validate
 ↓
Database
 ↓
Successful persistence
 ↓
Notify Sales
```

This prevents sales representatives from receiving leads that do not exist in the system.

---

# 19. WF-008 — Google Sheets Synchronization

After successful database persistence:

```text
PostgreSQL
     ↓
n8n
     ↓
Google Sheets
```

The sheet should contain operational fields such as:

```text
Lead ID
Customer Name
Phone
Email
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

# 20. Google Sheets Rule

Google Sheets is not the authoritative database.

If:

```text
PostgreSQL:
Budget = ₦80M

Google Sheets:
Budget = ₦70M
```

PostgreSQL is considered correct.

The synchronization workflow should update the sheet from the database.

---

# 21. WF-009 — Sales Notification

Notifications are triggered after successful lead processing.

### HOT Lead

Example notification:

```text
New HOT Lead — PrimeHomes

Customer: John Doe
Property: 3-bedroom apartment
Location: Lekki
Budget: ₦80M
Timeline: Within 2 months

Score: 90/100
Status: QUALIFIED

Please follow up with the customer.
```

---

# 22. Notification Channels

The first implementation can support:

```text
Email
```

Potential future channels:

```text
WhatsApp
Slack
Microsoft Teams
SMS
Push notifications
```

The architecture should allow additional notification nodes without rewriting the lead-processing workflow.

---

# 23. WF-010 — Generate Customer Response

The final response should be generated after processing.

The response depends on the state of the lead.

### Missing information

```text
Thanks. I can help with that. What's your budget range?
```

### Qualified

```text
Thanks, John. I've captured your requirements.

A member of our sales team will follow up with you shortly.
```

### Human requested

```text
I'll connect you with a member of our sales team.
```

---

# 24. Property Availability Rule

The bot must not say:

> "Yes, we have a 3-bedroom apartment available in Lekki for ₦80M."

unless the system has actually verified that information from an authoritative property inventory.

Without verified inventory, it should say something such as:

> "I've captured your requirements and our sales team can help you with matching properties."

This prevents hallucinated property listings.

---

# 25. Response Flow

```text
Lead Processing
      ↓
Determine Conversation State
      ↓
Missing Information?
   ↙             ↘
 YES              NO
 ↓                 ↓
Ask Question     Qualification
                    ↓
               Generate Response
                    ↓
              Return to FastAPI
                    ↓
                 React
```

---

# 26. WF-011 — Follow-Up Automation

This workflow runs on a schedule.

### Trigger

Schedule Trigger.

For example:

```text
Every 15 minutes
```

The workflow checks:

```text
Pending follow-ups
+
follow_up_date <= current time
```

---

# 27. Follow-Up Flow

```text
Schedule Trigger
      ↓
Get Pending Follow-Ups
      ↓
Filter Due Follow-Ups
      ↓
Notify Sales Rep
      ↓
Update Notification State
```

Example:

```text
Follow-up due:

Customer: John Doe
Lead: #123
Action: Call customer
Time: 10:00 AM
```

---

# 28. Overdue Follow-Ups

If a follow-up remains incomplete:

```text
PENDING
   ↓
Due
   ↓
OVERDUE
```

The system can notify the salesperson again according to configured rules.

It should avoid repeatedly notifying the salesperson every few minutes.

---

# 29. WF-012 — Error Handling

Every major workflow should have an error path.

General structure:

```text
Workflow
   ↓
Error?
 ┌─┴─────────┐
NO           YES
↓             ↓
Continue      Error Handler
              ↓
         Log Error
              ↓
       Record Request ID
              ↓
        Notify Admin
              ↓
      Retry / Escalate
```

---

# 30. Error Categories

The workflow should distinguish between:

### AI Error

```text
AI timeout
Invalid response
Malformed JSON
Rate limit
```

### Database Error

```text
Connection failure
Constraint violation
Timeout
```

### Google Sheets Error

```text
Authentication failure
Quota error
API timeout
```

### Notification Error

```text
Email failure
Invalid recipient
External service unavailable
```

### Application Error

```text
Invalid payload
Missing ID
Unexpected workflow state
```

---

# 31. Retry Strategy

Retries should be limited.

Recommended:

```text
Transient API failure
        ↓
Retry 1
        ↓
Retry 2
        ↓
If still failing
        ↓
Error Handler
```

Do not retry permanent validation errors.

For example:

```text
Invalid email
```

should not be retried indefinitely.

---

# 32. Idempotency

n8n workflows must be safe to retry.

For example:

```text
request_id = abc123
```

If the workflow receives the same request again:

```text
abc123
abc123
```

it should detect that the request has already been processed.

This is especially important for:

- Lead creation
- Notifications
- Google Sheets synchronization
- External webhooks

---

# 33. Workflow Separation

Do not build one massive n8n workflow containing everything.

Avoid:

```text
Webhook
 → AI
 → Database
 → Google Sheets
 → Email
 → Follow-up
 → Dashboard
 → Everything else
```

Instead use modular workflows:

```text
WF-001
WF-002
WF-003
...
WF-012
```

Workflows can call one another where appropriate.

This makes debugging and maintenance easier.

---

# 34. Recommended n8n Structure

```text
n8n/
│
├── Customer Processing
│   ├── WF-001 Receive Customer Message
│   ├── WF-002 Process Conversation
│   ├── WF-003 AI Extraction
│   ├── WF-004 Validate Data
│   └── WF-005 Missing Information
│
├── Lead Management
│   ├── WF-006 Qualification
│   ├── WF-007 Store Lead
│   └── WF-008 Google Sheets Sync
│
├── Communication
│   ├── WF-009 Sales Notification
│   └── WF-010 Customer Response
│
├── Scheduled
│   └── WF-011 Follow-Up
│
└── System
    └── WF-012 Error Handling
```

---

# 35. Credentials

Credentials must be stored securely in n8n.

Examples:

```text
AI API credential
Google credential
Email credential
FastAPI internal credential
Database credential, if direct DB access is required
```

Do not place API keys directly inside workflow nodes.

---

# 36. Environment Separation

Development and production credentials should be separate.

```text
Development
    ↓
Test APIs
Test database
Test Google Sheet
Test notifications
```

Production:

```text
Production API
Production database
Production Google Sheet
Production notifications
```

This prevents development testing from corrupting real data.

---

# 37. Logging

Important workflow events should include:

```text
request_id
conversation_id
message_id
lead_id
workflow_id
execution_id
timestamp
status
error_code
```

Avoid storing unnecessary sensitive customer data in logs.

---

# 38. Workflow Monitoring

The development process should monitor:

- Failed executions
- Slow executions
- AI failures
- Database failures
- Notification failures
- Google Sheets failures
- Retry counts

n8n execution history should be used during development and troubleshooting.

---

# 39. End-to-End Example

Customer sends:

> "Hi, I'm looking for a 3-bedroom apartment around Lekki. My budget is ₦80 million and I'd like to buy within two months."

### Step 1

React sends message.

```text
React
 ↓
FastAPI
```

### Step 2

FastAPI stores the message.

```text
FastAPI
 ↓
PostgreSQL
```

### Step 3

FastAPI triggers n8n.

```text
FastAPI
 ↓
WF-001
```

### Step 4

Conversation context is retrieved.

```text
WF-002
```

### Step 5

AI extracts:

```json
{
  "intent": "BUY",
  "property_type": "APARTMENT",
  "bedrooms": 3,
  "location": "Lekki",
  "budget_max": 80000000,
  "currency": "NGN",
  "timeline": "WITHIN_2_MONTHS"
}
```

### Step 6

Data is validated.

```text
WF-004
```

### Step 7

Lead is qualified.

```text
WF-006
```

Potential result:

```text
Score: 90
Temperature: HOT
```

### Step 8

Lead is persisted.

```text
WF-007
 ↓
PostgreSQL
```

### Step 9

Google Sheets is updated.

```text
WF-008
```

### Step 10

Sales team is notified.

```text
WF-009
```

### Step 11

Customer response is generated.

```text
WF-010
```

### Step 12

Response goes back through FastAPI.

```text
n8n
 ↓
FastAPI
 ↓
React
```

### Step 13

Customer sees:

> "Thanks. I've captured your requirements. A member of our sales team will follow up with you shortly."

---

# 40. Failure Scenario

Suppose Google Sheets is unavailable.

The correct behavior is:

```text
Customer
 ↓
AI
 ↓
Validation
 ↓
PostgreSQL
 ↓
SUCCESS
 ↓
Google Sheets
 ↓
FAIL
```

The lead should **remain safely stored in PostgreSQL**.

The Google Sheets synchronization should be retried separately.

The customer should not receive an error simply because the spreadsheet is temporarily unavailable.

---

# 41. Critical Architecture Rule

The workflow must prioritize:

```text
1. Receive
2. Validate
3. Persist
4. Process
5. Qualify
6. Notify
7. Synchronize
8. Respond
```

The exact technical implementation may optimize this sequence, but persistence must not be sacrificed for an external integration.

---

# 42. n8n Workflow Naming Convention

Use a consistent naming system:

```text
PRIMEHOMES | WF-001 | Receive Customer Message
PRIMEHOMES | WF-002 | Process Conversation
PRIMEHOMES | WF-003 | AI Lead Extraction
PRIMEHOMES | WF-004 | Validate Lead Data
PRIMEHOMES | WF-005 | Collect Missing Information
PRIMEHOMES | WF-006 | Qualify Lead
PRIMEHOMES | WF-007 | Store Lead
PRIMEHOMES | WF-008 | Google Sheets Sync
PRIMEHOMES | WF-009 | Sales Notification
PRIMEHOMES | WF-010 | Generate Customer Response
PRIMEHOMES | WF-011 | Follow-Up Automation
PRIMEHOMES | WF-012 | Error Handling
```

This will make the n8n workspace much easier to manage.

---

# 43. Development Order

When we eventually build the workflows, use this order:

```text
1. WF-001 Receive Customer Message
2. WF-002 Process Conversation
3. WF-003 AI Extraction
4. WF-004 Validation
5. WF-007 Store Lead
6. WF-006 Qualification
7. WF-010 Customer Response
8. WF-008 Google Sheets
9. WF-009 Sales Notification
10. WF-011 Follow-Up
11. WF-012 Error Handling
```

We should test each workflow before adding the next dependency.

---

# 44. Testing Requirements

Each workflow should be tested independently.

### Test 1 — Complete Lead

```text
3-bedroom
Lekki
₦80M
Buy
2 months
Phone
```

Expected:

```text
Lead created
HOT
Sales notified
Sheet updated
Customer receives response
```

### Test 2 — Incomplete Lead

```text
I want a house in Lekki.
```

Expected:

```text
Lead created/updated
Missing information identified
Bot asks next question
```

### Test 3 — Rental

```text
I want to rent a 2-bedroom apartment in Ikeja.
```

Expected:

```text
Intent = RENT
Transaction = RENT
```

### Test 4 — Land

```text
I need land around Ibadan below ₦20M.
```

Expected:

```text
Intent = LAND
Property = LAND
Location = Ibadan
Budget max = ₦20M
```

### Test 5 — AI Failure

Expected:

```text
Retry
 ↓
Error handling
 ↓
No corrupt lead
```

### Test 6 — Database Failure

Expected:

```text
Error recorded
 ↓
Notification suppressed
 ↓
Retry/escalation
```

### Test 7 — Duplicate Request

Expected:

```text
One lead
One processing event
No duplicate notification
```

---

# 45. Definition of Done

The n8n architecture is considered ready for implementation when:

- All workflows are defined.
- Workflow responsibilities are separated.
- Inputs and outputs are known.
- AI extraction is structured.
- Validation is defined.
- Lead qualification is defined.
- Database persistence is defined.
- Google Sheets synchronization is defined.
- Sales notifications are defined.
- Follow-up automation is defined.
- Error handling is defined.
- Retry strategy is defined.
- Idempotency is defined.
- Credential handling is defined.
- Logging requirements are defined.
- Testing scenarios are defined.
- Workflow naming conventions are defined.

---

# 46. Next Document

The next document should be:

## AI & Prompt Engineering Specification

That document will define the AI's exact role in the system, including:

- System prompt
- Lead extraction prompt
- Structured JSON schema
- Conversation context
- Missing-information logic
- Response-generation prompt
- Confidence handling
- Hallucination prevention
- Property availability rules
- Human escalation rules
- AI failure handling
- Model configuration

The goal is to make the AI a **controlled component of the system**, rather than allowing the LLM to make uncontrolled business decisions.