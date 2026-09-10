# PRODUCT REQUIREMENTS DOCUMENT (PRD)

## PrimeHomes Realty — Real Estate Lead Bot

**Document Version:** 1.0  
**Status:** Draft  
**Project Type:** Industry Project / MVP  
**Prepared By:** Product & Engineering Team  
**Date:** September 2026

---

# 1. Executive Summary

PrimeHomes Realty is a real estate company that receives potential customer enquiries through digital channels such as its website, chat interface, WhatsApp, email, and other lead sources.

As the number of enquiries increases, manually reading, extracting, qualifying, recording, and assigning leads becomes inefficient. This creates several business problems:

- Slow responses to potential customers.
- Inconsistent lead qualification.
- Missing or incomplete customer information.
- Leads being forgotten or poorly tracked.
- Sales staff spending time on administrative work.
- High-value opportunities not being prioritized appropriately.
- Limited visibility into the status of each lead.

The proposed solution is the **PrimeHomes Realty Lead Bot**, an intelligent lead-management system that acts as a digital receptionist.

The system will receive customer enquiries, understand their intent, extract relevant information, qualify the lead, store the information, respond to the customer, notify the sales team, and track the lead throughout the sales process.

The system will use:

- **React** for the customer-facing frontend.
- **FastAPI/Python** for the backend API and custom business logic.
- **n8n** as the workflow automation and orchestration engine.
- **Google Sheets** for operational visibility and selected n8n-based data operations.
- **SQL database** as the structured system of record for leads and their lifecycle data.
- **AI** for natural-language understanding, information extraction, classification, summarization, and response generation.

The initial goal is to build a reliable MVP that demonstrates the complete lead lifecycle from first customer enquiry through sales follow-up.

---

# 2. Product Vision

Build a reliable digital receptionist for PrimeHomes Realty that can automatically turn unstructured customer enquiries into actionable, qualified sales leads.

The system should allow a customer to communicate naturally while allowing the business to receive structured, prioritized, and trackable lead information.

### Vision

> "Every customer enquiry should be captured, understood, qualified, responded to, and made actionable for the sales team."

---

# 3. Business Problem

PrimeHomes Realty may receive hundreds of enquiries from potential customers.

Examples include:

> "Hi, I'm looking for a 3-bedroom apartment around Lekki. My budget is around ₦80 million."

> "Do you have any 2-bedroom apartments in Ikeja?"

> "I need land around Ibadan, preferably below ₦20 million."

> "Hello, I want to buy a house."

These messages contain useful information, but the information is often unstructured.

A salesperson may need to manually identify:

- Customer name.
- Phone number.
- Email address.
- Property type.
- Location.
- Number of bedrooms.
- Budget.
- Buying or renting.
- Timeline.
- Customer intent.
- Level of interest.

At scale, this manual process can result in delays, inconsistent data, missed leads, and lost sales opportunities.

---

# 4. Product Goals

The MVP should achieve the following goals.

## 4.1 Lead Capture

Allow potential customers to submit property enquiries through the React interface.

## 4.2 Intelligent Understanding

Use AI to understand natural-language customer messages.

## 4.3 Information Extraction

Convert unstructured messages into structured lead information.

## 4.4 Lead Qualification

Calculate a lead score based on predefined business rules.

## 4.5 Lead Storage

Store lead information in a SQL database.

## 4.6 Operational Visibility

Synchronize appropriate lead information with Google Sheets so the business can easily inspect and manage leads through tools already familiar to them.

## 4.7 Automated Response

Provide customers with an appropriate response based on the information available.

## 4.8 Sales Notification

Notify the sales team when a lead requires attention, particularly high-priority leads.

## 4.9 Lead Tracking

Track the status of a lead from initial enquiry through follow-up.

## 4.10 Extensibility

Design the MVP so additional communication channels, CRM integrations, property search, analytics, and advanced AI capabilities can be added later.

---

# 5. Product Scope

## 5.1 In Scope — MVP

The MVP will include:

1. Customer chat/lead interface.
2. Lead submission.
3. Customer information collection.
4. Natural-language message processing.
5. AI-powered information extraction.
6. Missing-information detection.
7. Lead qualification.
8. Lead scoring.
9. Hot/Warm/Cold classification.
10. SQL lead storage.
11. Google Sheets synchronization.
12. Automated customer response.
13. Sales team notification.
14. Lead status tracking.
15. Basic sales follow-up workflow.
16. Error handling.
17. Basic logging.
18. Testing of common and failure scenarios.

---

# 6. Out of Scope — MVP

The following will not be required for the first version unless explicitly added later:

- Full CRM replacement.
- Advanced property recommendation engine.
- Automated property transactions.
- Online payment processing.
- Property booking/payment.
- Mortgage processing.
- Contract generation.
- Legal documentation.
- Advanced sales forecasting.
- Fully autonomous sales negotiation.
- Complex multi-agent AI architecture.
- Native mobile applications.
- Large-scale analytics platform.

These may become future product capabilities.

---

# 7. Target Users

## 7.1 Potential Customer

A person interested in buying, renting, or enquiring about real estate.

The customer should be able to communicate naturally without needing to understand the underlying system.

### Primary needs

- Easily submit an enquiry.
- Explain what they are looking for.
- Receive a quick response.
- Avoid repeatedly providing the same information.
- Get connected to a sales representative when necessary.

---

## 7.2 Sales Representative

A member of the PrimeHomes Realty sales team responsible for following up with leads.

### Primary needs

- Receive new leads quickly.
- Know what the customer wants.
- See lead priority.
- See customer contact information.
- Know when the customer wants to buy/rent.
- Track follow-up activity.
- Update lead status.

---

## 7.3 Sales Manager

A manager responsible for monitoring sales activity and lead distribution.

### Primary needs

- See incoming leads.
- Identify high-value opportunities.
- Monitor lead status.
- Track sales-team follow-up.
- Identify leads that have not been contacted.
- Monitor overall lead pipeline.

---

## 7.4 System Administrator

A technical/business administrator responsible for system configuration.

### Primary needs

- Configure business rules.
- Manage integrations.
- Monitor automation failures.
- Maintain system configuration.

---

# 8. Core User Journey

The expected customer journey is:

```text
Customer
   ↓
Opens Lead Bot
   ↓
Sends enquiry
   ↓
System receives message
   ↓
AI understands enquiry
   ↓
Information is extracted
   ↓
System checks missing information
   ↓
Customer provides missing information
   ↓
Lead is qualified
   ↓
Lead score calculated
   ↓
Lead stored
   ↓
Sales team notified
   ↓
Customer receives response
   ↓
Sales representative follows up
   ↓
Lead status updated
```

---

# 9. Functional Requirements

## FR-001 — Customer Enquiry Submission

The system shall allow customers to submit a property enquiry through the React frontend.

### Acceptance Criteria

- Customer can open the lead interface.
- Customer can enter a message.
- Customer can submit the message.
- The system sends the message to the backend.
- The customer receives a system response.

---

## FR-002 — Customer Information Collection

The system shall collect available customer information.

Possible information includes:

- Name.
- Email.
- Phone number.

The system should not require all information to be available in the first message.

### Acceptance Criteria

If information is missing, the system should identify what is required and request it appropriately.

Example:

Customer:

> "I need a 3-bedroom apartment in Lekki."

Bot:

> "I'd be happy to help. What's your approximate budget, and when are you looking to move?"

---

# 10. Property Requirement Extraction

The system shall identify relevant property requirements from customer messages.

The system should attempt to extract:

| Field | Example |
|---|---|
| Property type | Apartment |
| Bedrooms | 3 |
| Location | Lekki |
| Budget | ₦80,000,000 |
| Transaction type | Buy |
| Timeline | Within 2 months |

The system should support information expressed naturally.

Example:

> "I have around 80m and want something with three bedrooms in Lekki."

Should produce structured information equivalent to:

```text
property_type: apartment
bedrooms: 3
location: Lekki
budget: 80000000
transaction_type: buy
```

Where information cannot be confidently determined, the system should not invent a value.

---

# 11. Customer Intent Detection

The system shall identify the customer's primary intent.

Supported MVP intents:

- Buying property.
- Renting property.
- Selling property.
- Land enquiry.
- Property enquiry.
- General enquiry.

Example:

> "I need land around Ibadan."

Intent:

```text
land_enquiry
```

---

# 12. Timeline Detection

The system should identify the customer's expected timeframe.

Supported categories:

- Immediately.
- Within 1 month.
- Within 3 months.
- More than 3 months.
- Just researching.
- Unknown.

The system should also understand natural language such as:

> "I need something this month."

or:

> "I'm just checking prices for now."

---

# 13. Missing Information Detection

The system shall determine whether sufficient information is available to qualify a lead.

For example:

Customer:

> "I want to buy a house."

The system may need to ask:

- What location?
- What type of property?
- What is your budget?
- How many bedrooms?
- When are you looking to buy?

The bot should ask questions progressively rather than overwhelming the customer with a long form.

---

# 14. Lead Qualification

The system shall determine the potential value and urgency of a lead.

The MVP will use a rule-based scoring system supported by structured information extracted by AI.

### Example scoring rules

| Condition | Points |
|---|---:|
| Phone number provided | +10 |
| Budget provided | +20 |
| Location provided | +15 |
| Property type provided | +15 |
| Buying/renting timeline is soon | +25 |
| Clear property requirements | +15 |

### Lead classification

| Score | Classification |
|---:|---|
| 80–100 | HOT |
| 50–79 | WARM |
| 0–49 | COLD |

These values are initial business rules and should be configurable in the future.

---

# 15. Lead Storage

Every qualified lead shall be stored in the SQL database.

At minimum, a lead should contain:

### Customer information

- Lead ID.
- Name.
- Email.
- Phone.

### Property requirements

- Property type.
- Bedrooms.
- Location.
- Budget.
- Transaction type.
- Timeline.

### Qualification

- Lead score.
- Lead classification.
- Qualification reason.

### Lifecycle

- Lead status.
- Assigned sales representative.
- Created timestamp.
- Updated timestamp.
- Last contact timestamp.

---

# 16. Google Sheets Integration

Google Sheets will be used as an operational interface and integration layer for selected workflows.

The SQL database remains the authoritative structured database for the application.

Google Sheets may be used for:

- Operational lead visibility.
- Sales-team access.
- Simple reporting.
- Manual updates where appropriate.
- n8n workflow integration.
- Demonstration and testing.

The system should avoid creating conflicting sources of truth.

### Principle

```text
SQL Database
    ↓
Primary System of Record

Google Sheets
    ↓
Operational / Integration View
```

If a conflict occurs between the two systems, the defined system-of-record policy should determine which value is authoritative.

---

# 17. Automated Customer Response

The system shall generate an appropriate response after processing a customer enquiry.

The response should:

- Acknowledge the customer.
- Reflect their requirements where appropriate.
- Ask for missing information when necessary.
- Avoid inventing property availability.
- Avoid making promises the system cannot guarantee.
- Escalate to a human representative when appropriate.

Example:

> "Thanks for your enquiry. I understand you're looking for a 3-bedroom apartment in Lekki with a budget of around ₦80 million. When are you hoping to move?"

---

# 18. Sales Notification

The system shall notify the sales team when a lead requires attention.

High-priority leads should receive more urgent notification.

Example:

```text
NEW HOT LEAD

Name: John Doe
Property: 4-bedroom apartment
Location: Lekki
Budget: ₦100M
Timeline: This month
Score: 90
Priority: HOT
```

The specific notification channel can initially be implemented through the integrations available in n8n.

Potential channels include:

- Email.
- WhatsApp.
- Slack.
- Other business messaging platforms.

---

# 19. Lead Assignment

The system should support assigning leads to sales representatives.

For the MVP, assignment may use a simple rule such as:

- Manual assignment.
- Round-robin assignment.
- Location-based assignment.

The exact assignment strategy can be finalized during system design.

---

# 20. Lead Lifecycle

A lead shall have a defined lifecycle.

Recommended MVP statuses:

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

Alternative terminal states:

```text
LOST
CLOSED
UNQUALIFIED
```

The system should maintain a history of important status changes.

---

# 21. Sales Follow-Up

Sales representatives should be able to follow up with leads.

The system should support:

- Viewing lead details.
- Seeing lead priority.
- Seeing customer requirements.
- Seeing previous interaction information.
- Updating lead status.
- Recording follow-up.
- Setting a follow-up date/time.

Future versions may automate follow-up reminders.

---

# 22. Conversation Context

The bot should maintain enough conversation context to avoid repeatedly asking for information already provided.

Example:

Customer:

> "I want a house in Lekki."

Bot:

> "What's your budget?"

Customer:

> "Around ₦80 million."

The system should understand that:

```text
location = Lekki
budget = ₦80,000,000
```

and retain both values.

---

# 23. AI Requirements

AI shall be used primarily for language understanding and generation.

AI responsibilities include:

1. Understanding customer messages.
2. Extracting structured information.
3. Detecting intent.
4. Detecting missing information.
5. Classifying conversation context.
6. Generating customer responses.
7. Summarizing conversations.

AI shall not independently determine business-critical outcomes without defined system rules.

For example:

```text
AI
 ↓
Extract structured information
 ↓
Business rules
 ↓
Lead score
```

rather than:

```text
AI
 ↓
"Trust me, this is a hot lead."
```

This separation improves predictability and makes the system easier to test.

---

# 24. n8n Requirements

n8n shall act as the primary workflow orchestration layer.

Responsibilities include:

- Receiving webhook requests.
- Triggering AI processing.
- Calling backend APIs where necessary.
- Processing structured data.
- Applying workflow logic.
- Writing to databases.
- Synchronizing Google Sheets.
- Sending notifications.
- Triggering follow-up workflows.
- Handling integrations.
- Logging workflow execution outcomes.

n8n should not become the location for every piece of application logic.

Complex or reusable business logic may be implemented in the FastAPI backend.

---

# 25. FastAPI Backend Requirements

The FastAPI backend shall provide application APIs and custom backend functionality.

Potential endpoints include:

```text
POST /api/leads
GET /api/leads/{lead_id}
PATCH /api/leads/{lead_id}
POST /api/chat
GET /api/leads
POST /api/leads/{lead_id}/follow-up
```

The final API contract will be defined in the API Specification/System Design document.

FastAPI may handle:

- Request validation.
- Authentication/authorization where required.
- Data validation.
- Custom business rules.
- Database interaction.
- Specialized calculations.
- API integrations.
- Backend services that should not live inside n8n.

---

# 26. React Frontend Requirements

The React application shall provide the customer-facing interface.

The initial interface should include:

### Customer Chat

- Message input.
- Conversation display.
- Send action.
- Loading state.
- Error state.

### Lead Information

Where appropriate, the interface may display or request:

- Name.
- Email.
- Phone.
- Property requirements.

### Future Sales Interface

A future React dashboard may provide:

- Lead list.
- Lead details.
- Lead score.
- Lead status.
- Assignment.
- Follow-up management.

The customer-facing interface and internal sales dashboard should be architecturally separable.

---

# 27. Non-Functional Requirements

## NFR-001 — Performance

The system should provide a reasonably fast response to customers.

Target for MVP:

- Initial API response should normally be under 2 seconds excluding external AI/integration latency.
- AI responses should be monitored separately because model response time may vary.

---

## NFR-002 — Reliability

A failure in one integration should not silently lose a lead.

For example:

```text
Lead received
      ↓
Database save
      ↓
Notification fails
```

The lead should remain stored and the notification failure should be logged and recoverable.

---

## NFR-003 — Security

The system shall protect customer information.

Requirements include:

- HTTPS for production communication.
- Secure API credentials.
- Environment variables/secrets for sensitive credentials.
- No API keys hard-coded into source code.
- Appropriate authentication for internal APIs.
- Input validation.
- Protection against unauthorized access.

---

## NFR-004 — Data Integrity

Lead records should not be duplicated unnecessarily.

The system should support identifying leads using appropriate identifiers such as:

- Lead ID.
- Customer contact information.
- Conversation/session ID.

---

## NFR-005 — Maintainability

The system should use clear separation of responsibilities:

```text
React
  ↓
FastAPI
  ↓
n8n
  ↓
AI / Database / Integrations
```

Components should be independently testable where practical.

---

## NFR-006 — Observability

The system should record sufficient information to investigate failures.

Important events include:

- Lead received.
- AI processing started.
- AI processing completed.
- Lead saved.
- Notification sent.
- Notification failed.
- Lead status changed.
- Workflow failed.

---

## NFR-007 — Scalability

The architecture should allow the system to handle increasing numbers of leads without requiring a complete redesign.

The MVP does not need enterprise-scale infrastructure, but major components should not be tightly coupled unnecessarily.

---

# 28. Error Handling Requirements

The system must gracefully handle:

### Missing customer information

Ask the customer for the required information.

### Invalid information

Ask the customer to clarify.

### AI failure

The system should fall back to an appropriate response or route the enquiry for human handling.

### Database failure

The system should log the failure and prevent silent data loss.

### n8n workflow failure

The failed workflow should be identifiable and recoverable.

### External API failure

The system should handle timeouts and failed requests appropriately.

---

# 29. Business Rules

Initial business rules include:

### Rule 1 — Do not invent customer information

If the customer has not provided a budget, the system should not assume one.

### Rule 2 — Do not invent property availability

The bot should not tell a customer that a property is available unless availability has been verified from an appropriate source.

### Rule 3 — Prioritize urgent high-value leads

Leads with strong requirements, significant budgets, and short timelines should receive higher priority.

### Rule 4 — Human escalation

The system should allow escalation to a sales representative when:

- The customer explicitly asks for a human.
- The enquiry is complex.
- The AI cannot confidently understand the request.
- The customer is highly qualified.
- A workflow/system failure occurs.

### Rule 5 — Database authority

SQL is the primary system of record for application data.

Google Sheets is primarily an operational/integration layer unless a specific workflow explicitly defines otherwise.

---

# 30. Lead Data Requirements

The MVP lead record should conceptually contain:

```text
Lead
├── id
├── customer
│   ├── name
│   ├── email
│   └── phone
│
├── requirements
│   ├── property_type
│   ├── bedrooms
│   ├── location
│   ├── budget
│   ├── transaction_type
│   └── timeline
│
├── intent
├── lead_score
├── lead_temperature
├── status
├── assigned_sales_rep
│
├── conversation
│   ├── conversation_id
│   └── summary
│
├── created_at
├── updated_at
└── last_contacted_at
```

The exact relational schema will be defined in the Database Design document.

---

# 31. User Stories

## Customer

### US-001

As a potential customer, I want to send a natural-language enquiry so that I can explain what property I am looking for without filling out a complicated form.

### US-002

As a potential customer, I want the bot to ask me for missing information so that my enquiry can be properly understood.

### US-003

As a potential customer, I want to receive a quick response after submitting an enquiry.

### US-004

As a potential customer, I want to speak with a human representative when necessary.

---

## Sales Representative

### US-005

As a sales representative, I want to receive new qualified leads so that I can follow up quickly.

### US-006

As a sales representative, I want to see the customer's requirements so that I know what to discuss.

### US-007

As a sales representative, I want to see the lead score so that I can prioritize my work.

### US-008

As a sales representative, I want to update lead status so that the sales pipeline remains accurate.

### US-009

As a sales representative, I want to record follow-up information so that customer interactions are not lost.

---

## Sales Manager

### US-010

As a sales manager, I want to see high-value leads so that my team can prioritize important opportunities.

### US-011

As a sales manager, I want to know which leads have not been contacted so that opportunities are not forgotten.

### US-012

As a sales manager, I want to monitor lead statuses so that I can understand the sales pipeline.

---

# 32. MVP Success Criteria

The MVP will be considered successful when the following end-to-end scenario works reliably:

### Scenario

Customer sends:

> "Hi, I'm looking for a 3-bedroom apartment around Lekki. My budget is around ₦80 million and I want to buy within the next two months."

The system should:

1. Receive the message.
2. Validate the request.
3. Process it through the workflow.
4. Extract:
   - Property type.
   - Bedrooms.
   - Location.
   - Budget.
   - Transaction type.
   - Timeline.
5. Calculate the lead score.
6. Classify the lead.
7. Store the lead in SQL.
8. Synchronize appropriate information to Google Sheets.
9. Generate a customer response.
10. Notify the appropriate sales channel/team.
11. Allow the sales team to follow up.
12. Allow the lead status to be updated.
13. Preserve the lead record throughout the lifecycle.

---

# 33. MVP Acceptance Criteria

The MVP must demonstrate that:

- A customer can submit an enquiry.
- The frontend communicates successfully with the backend.
- FastAPI validates incoming requests.
- n8n can receive/process the workflow.
- AI can extract structured requirements.
- Missing information can be detected.
- A lead score can be calculated.
- Leads can be classified as HOT, WARM, or COLD.
- Leads can be stored in SQL.
- Lead information can be synchronized to Google Sheets.
- Customers receive automated responses.
- Sales staff receive notifications.
- Leads have trackable statuses.
- Failed workflows are identifiable.
- Sensitive credentials are not hard-coded.
- The system handles incomplete customer messages.
- The system does not invent unavailable property information.

---

# 34. Example End-to-End Scenarios

## Scenario A — Complete High-Value Lead

Customer:

> "I need a 4-bedroom house in Lekki. My budget is ₦100 million and I want to buy this month."

Expected result:

```text
Property: House
Bedrooms: 4
Location: Lekki
Budget: ₦100,000,000
Transaction: Buy
Timeline: Within 1 month

Priority: HOT
```

Sales team should receive a high-priority notification.

---

## Scenario B — Incomplete Lead

Customer:

> "I want to buy a house."

Expected behavior:

The bot should request additional information instead of immediately creating a fully qualified lead.

Possible questions:

- Preferred location?
- Property type?
- Budget?
- Number of bedrooms?
- Expected purchase timeline?

---

## Scenario C — Rental Lead

Customer:

> "I'm looking for a 2-bedroom apartment in Ikeja. My budget is ₦3 million yearly and I need it next month."

Expected result:

```text
Property: Apartment
Bedrooms: 2
Location: Ikeja
Budget: ₦3,000,000/year
Transaction: Rent
Timeline: Within 1 month
```

---

## Scenario D — Land Enquiry

Customer:

> "I need land around Ibadan, preferably below ₦20 million."

Expected result:

```text
Property: Land
Location: Ibadan
Budget: ₦20,000,000 maximum
Intent: Land enquiry
```

The system should request additional information if required for qualification.

---

## Scenario E — Human Escalation

Customer:

> "I want to speak with an agent."

Expected behavior:

The system should recognize the request and initiate the appropriate human handoff workflow.

---

# 35. Product Architecture Principle

The product should follow a clear separation of responsibilities.

```text
CUSTOMER
    ↓
REACT FRONTEND
    ↓
FASTAPI
    ↓
n8n
    ↓
┌───────────────┬───────────────┬───────────────┐
│               │               │
AI              SQL             Integrations
│               │               │
│               │               ├── Google Sheets
│               │               ├── Notifications
│               │               └── Other services
│               │
└───────────────┴───────────────┘
                ↓
           SALES TEAM
```

The architecture should avoid making any single technology responsible for everything.

---

# 36. Technology Responsibilities

| Component | Primary Responsibility |
|---|---|
| React | Customer interface |
| FastAPI | Backend API and custom application logic |
| n8n | Workflow orchestration and integrations |
| AI | Language understanding and generation |
| SQL | Primary structured data store |
| Google Sheets | Operational visibility/integration |
| Notification service | Sales alerts |
| Git | Source-code/version control |

---

# 37. Security & Privacy Considerations

The system will process customer information such as names, phone numbers, email addresses, property requirements, and potentially financial/budget information.

Therefore:

- Customer data should be transmitted securely.
- Credentials should be stored securely.
- API keys should not be committed to Git.
- Access to internal lead information should be restricted.
- Logs should avoid exposing unnecessary sensitive information.
- Database access should use controlled credentials.
- Production secrets should be separated from development configuration.

The production security model will be defined in the technical design and deployment documentation.

---

# 38. Assumptions

This PRD currently assumes:

1. PrimeHomes Realty has permission to collect and process customer enquiries.
2. Customers voluntarily provide information.
3. The company has at least one sales representative.
4. SQL will be the primary application database.
5. Google Sheets is required for operational visibility/integration.
6. n8n will be available as the automation platform.
7. AI services will be available through an API.
8. The MVP will initially focus on a limited number of communication channels.
9. Property availability will not be fabricated by the AI.
10. The first version will prioritize reliability and clear workflows over advanced AI autonomy.

---

# 39. Key Risks

| Risk | Impact | Mitigation |
|---|---|---|
| AI extracts incorrect information | High | Structured output + validation |
| AI hallucinates property availability | High | Restrict AI from claiming availability without verified data |
| Duplicate leads | Medium | Lead/conversation identifiers and deduplication |
| n8n workflow failure | High | Error handling and logging |
| Google Sheets becomes inconsistent with SQL | Medium | Define SQL as system of record |
| Customer provides incomplete information | Medium | Progressive questioning |
| External API failure | High | Retry/fallback mechanisms |
| Sensitive data exposure | High | Secure credentials and access controls |
| Overly complex workflow | Medium | Keep responsibilities clearly separated |
| Poor sales follow-up | High | Status tracking and follow-up reminders |

---

# 40. Future Enhancements

After the MVP, the product could be extended with:

### Property Matching

Automatically match customer requirements with available properties.

### CRM Integration

Integrate with a dedicated CRM.

### WhatsApp

Allow customers to communicate through WhatsApp.

### Email Integration

Process leads arriving through email.

### Advanced Lead Scoring

Use historical conversion data to improve qualification.

### Sales Dashboard

Build a full React-based sales dashboard.

### Automated Follow-Ups

Automatically remind customers and sales representatives.

### Analytics

Track:

- Lead volume.
- Conversion rate.
- Response time.
- Sales representative performance.
- Lead source.
- Hot-lead conversion.
- Lost leads.

### AI Conversation Summaries

Generate concise summaries for sales representatives.

### Multi-Channel Lead Capture

```text
Website
WhatsApp
Instagram
Email
Facebook
        ↓
     Lead Bot
        ↓
      n8n
        ↓
    Lead System
```

---

# 41. Definition of Done — MVP

The project will be considered complete when:

- The React application is functional.
- FastAPI APIs are implemented and documented.
- n8n workflows are operational.
- AI extraction is working with structured output.
- SQL database is implemented.
- Google Sheets integration is working.
- Lead scoring is implemented.
- Lead statuses are implemented.
- Sales notifications are working.
- Customer responses are working.
- Error handling is implemented.
- Core workflows are tested.
- The system can demonstrate the complete lead lifecycle.
- Documentation exists for setup, architecture, APIs, database, n8n workflows, and deployment.

---

# 42. Product Definition

The PrimeHomes Realty Lead Bot is not simply an AI chatbot.

It is a **lead-management and sales-automation system**.

Its core flow is:

```text
CAPTURE
   ↓
UNDERSTAND
   ↓
EXTRACT
   ↓
VALIDATE
   ↓
QUALIFY
   ↓
STORE
   ↓
RESPOND
   ↓
NOTIFY
   ↓
FOLLOW UP
   ↓
TRACK
   ↓
CONVERT
```

The product succeeds when a raw customer message becomes a structured, actionable sales opportunity without requiring a salesperson to manually perform every step.