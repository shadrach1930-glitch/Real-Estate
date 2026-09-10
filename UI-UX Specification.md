# PrimeHomes Realty Real Estate Lead Bot
## UI/UX Specification

**Document Version:** 1.0  
**Project:** PrimeHomes Realty Real Estate Lead Bot  
**Status:** Ready for Development  
**Frontend:** React  
**Backend:** FastAPI  
**Primary Users:** Customers and Sales Representatives  

---

# 1. Purpose

This document defines the user interface and user experience for the PrimeHomes Realty Real Estate Lead Bot.

The system has two primary interfaces:

1. **Customer-facing chat interface**
2. **Internal sales dashboard**

The customer interface focuses on making property enquiries simple and conversational.

The sales dashboard focuses on helping sales representatives quickly understand, prioritize and manage leads.

---

# 2. UX Goals

The interface should be:

- Simple
- Professional
- Fast
- Mobile-friendly
- Easy to understand
- Accessible to non-technical users
- Focused on lead conversion
- Consistent across screens

The customer should not feel like they are filling out a complicated CRM form.

The interaction should feel like:

```text
Customer
   ↓
"Hi, I want a 3-bedroom apartment in Lekki."
   ↓
Bot
   ↓
"Sure. What's your budget?"
```

Rather than:

```text
Property Type: [Dropdown]
Bedrooms: [Input]
Location: [Input]
Budget: [Input]
Timeline: [Dropdown]
...
```

The bot can collect these details conversationally.

---

# 3. User Types

## 3.1 Customer

The customer wants to:

- Ask about properties
- State their requirements
- Provide contact information
- Receive assistance
- Request a human representative
- Continue a conversation

## 3.2 Sales Representative

The salesperson wants to:

- View leads
- Prioritize hot leads
- See customer requirements
- Read conversations
- Contact customers
- Create follow-ups
- Update lead status
- Track lead progress

## 3.3 Administrator

An administrator may eventually manage:

- Sales representatives
- Lead assignment rules
- System configuration
- Analytics
- Integrations

The initial version may not require a dedicated admin interface.

---

# 4. Application Structure

The application will have two major areas.

```text
PrimeHomes
│
├── Customer Experience
│   └── Chat
│
└── Sales Portal
    ├── Dashboard
    ├── Leads
    ├── Lead Details
    ├── Conversations
    └── Follow-Ups
```

---

# 5. Customer Experience

## Screen: Customer Chat

The chat interface is the primary customer-facing experience.

### Layout

```text
┌───────────────────────────────────────┐
│ PrimeHomes Realty              Menu   │
├───────────────────────────────────────┤
│                                       │
│   PrimeHomes Assistant                │
│   How can we help you today?          │
│                                       │
│          ┌──────────────────────┐     │
│          │ I want a 3-bedroom   │     │
│          │ apartment in Lekki.  │     │
│          └──────────────────────┘     │
│                                       │
│ ┌───────────────────────────────────┐ │
│ │ Great. What's your budget range? │ │
│ └───────────────────────────────────┘ │
│                                       │
├───────────────────────────────────────┤
│ Type your message...          [Send] │
└───────────────────────────────────────┘
```

---

# 6. Customer Chat Header

The header should contain:

- PrimeHomes logo/name
- Assistant label
- Optional online/available indicator
- Minimal navigation

Example:

```text
PrimeHomes Realty
AI Property Assistant
```

Avoid excessive navigation on the customer screen.

The goal is to keep the customer focused on the conversation.

---

# 7. Welcome Message

When a new customer opens the chat:

```text
Welcome to PrimeHomes Realty.

I'm here to help you find the right property.

You can tell me what you're looking for, your preferred location, budget, or whether you're buying or renting.
```

Suggested quick actions:

```text
[Buy a property]
[Rent a property]
[Find land]
[Speak to an agent]
```

These buttons are optional shortcuts.

The customer should still be able to type freely.

---

# 8. Message Bubbles

Messages should visually distinguish between:

### Customer

Right aligned.

```text
                  ┌─────────────────────┐
                  │ I need a 3-bedroom   │
                  │ apartment in Lekki.  │
                  └─────────────────────┘
```

### Bot

Left aligned.

```text
┌──────────────────────────────────────┐
│ Great. What budget are you working   │
│ with?                                │
└──────────────────────────────────────┘
```

### Sales Representative

If a human joins:

```text
Sarah — PrimeHomes Sales

┌──────────────────────────────────────┐
│ Hi John, I'm Sarah from PrimeHomes.  │
│ I'll be assisting you from here.    │
└──────────────────────────────────────┘
```

---

# 9. Typing Indicator

When the AI is processing:

```text
PrimeHomes Assistant
● ● ●
```

This gives the customer immediate feedback.

The interface should not appear frozen while waiting for a response.

---

# 10. Error State

If the system cannot process the request:

```text
Sorry, I'm having trouble processing that message right now.

Please try again or request to speak with a sales representative.
```

Buttons:

```text
[Try Again]
[Speak to an Agent]
```

The customer should never see technical errors such as:

```text
500 Internal Server Error
Database connection failed
n8n webhook timeout
```

---

# 11. Human Escalation

The customer should be able to request a human.

Example:

```text
[Speak to a Human Agent]
```

When selected:

```text
I'll connect you with a member of our sales team.

Could you please provide your name and phone number so they can contact you?
```

The lead should be flagged for human intervention.

---

# 12. Customer Information Collection

The system should collect information progressively.

Example conversation:

```text
Customer:
I need a house.

Bot:
Sure. Are you looking to buy or rent?

Customer:
Buy.

Bot:
What location are you interested in?

Customer:
Lekki.

Bot:
What type of property are you looking for?

Customer:
4-bedroom house.

Bot:
What's your approximate budget?
```

The UI should not repeatedly ask for information already provided.

---

# 13. Contact Information Collection

When appropriate, the bot should request:

- Name
- Phone
- Email

Example:

```text
Thanks. I've got your property requirements.

What name should I use for your enquiry?
```

Then:

```text
And what phone number can our sales team use to contact you?
```

---

# 14. Lead Capture Confirmation

Once sufficient information has been collected:

```text
Thanks, John.

I've captured your requirements:

3-bedroom apartment
Lekki
Budget: ₦80 million
Buying within 2 months

A member of our sales team will follow up with you shortly.
```

This gives the customer confidence that the information was recorded correctly.

---

# 15. Sales Dashboard

The sales dashboard is the main internal application.

### Desktop layout

```text
┌──────────────────────────────────────────────────────────────┐
│ PrimeHomes                         Sarah ▼    Notifications   │
├────────────┬─────────────────────────────────────────────────┤
│            │                                                 │
│ Dashboard  │  Overview                                       │
│            │                                                 │
│ Leads      │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐  │
│            │  │ Total  │ │  Hot   │ │  Warm  │ │Converted│ │
│ Follow-ups │  │  250   │ │   42   │ │   98   │ │   25   │  │
│            │  └────────┘ └────────┘ └────────┘ └────────┘  │
│ Settings   │                                                 │
│            │  Recent Leads                                  │
│            │  ┌───────────────────────────────────────────┐ │
│            │  │ John Doe   3BR   Lekki   ₦80M   HOT       │ │
│            │  │ Mary Jane  2BR   Ikeja   ₦45M   WARM      │ │
│            │  └───────────────────────────────────────────┘ │
│            │                                                 │
└────────────┴─────────────────────────────────────────────────┘
```

---

# 16. Dashboard Navigation

The sidebar should contain:

```text
Dashboard
Leads
Follow-ups
Conversations
Settings
```

Depending on the final scope, Conversations can also be accessed through individual lead records rather than being a separate page.

---

# 17. Dashboard Summary Cards

The dashboard should show key metrics.

Recommended cards:

```text
Total Leads
New Leads
Hot Leads
Warm Leads
Qualified Leads
Converted Leads
Pending Follow-ups
```

Example:

```text
┌────────────────┐
│ HOT LEADS      │
│      42        │
│ ↑ 12%          │
└────────────────┘
```

The first version does not need advanced analytics.

---

# 18. Lead List Screen

## Route

```text
/leads
```

The lead list should allow sales representatives to quickly scan opportunities.

### Columns

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

Example:

```text
┌──────────────────────────────────────────────────────────────┐
│ Leads                                                        │
├──────────────────────────────────────────────────────────────┤
│ Search leads...     [Status ▼] [Temperature ▼] [Intent ▼]  │
├──────────────────────────────────────────────────────────────┤
│ John Doe     3BR Apartment   Lekki   ₦80M   90  HOT         │
│ Mary Jane    2BR Apartment   Ikeja   ₦45M   70  WARM        │
│ David Smith  Land            Ibadan  ₦18M   55  WARM        │
└──────────────────────────────────────────────────────────────┘
```

---

# 19. Lead Filtering

The interface should support:

### Status

```text
NEW
QUALIFIED
ASSIGNED
CONTACTED
FOLLOW_UP
NEGOTIATION
CONVERTED
LOST
```

### Temperature

```text
HOT
WARM
COLD
```

### Intent

```text
BUY
RENT
SELL
LAND
PROPERTY_ENQUIRY
```

### Assignment

```text
All
My Leads
Unassigned
Specific Sales Rep
```

---

# 20. Lead Search

Search should support:

- Customer name
- Phone
- Email
- Lead ID
- Location

Example:

```text
Search: "John"
```

Returns matching leads.

---

# 21. Lead Details Page

## Route

```text
/leads/{lead_id}
```

This is one of the most important internal screens.

### Layout

```text
┌──────────────────────────────────────────────────────────────┐
│ ← Leads                                      HOT   Score 90  │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ John Doe                                  [Contact Customer] │
│ +234 801 234 5678                                           │
│ john@example.com                                             │
│                                                              │
├───────────────────────────┬──────────────────────────────────┤
│ Property Requirements     │ Lead Information                │
│                           │                                  │
│ Property: Apartment       │ Status: QUALIFIED               │
│ Bedrooms: 3               │ Temperature: HOT                │
│ Location: Lekki           │ Score: 90                        │
│ Budget: ₦80,000,000       │ Intent: BUY                     │
│                           │ Timeline: 2 months              │
├───────────────────────────┴──────────────────────────────────┤
│                                                              │
│ Conversation                                                │
│                                                              │
│ Customer: I'm looking for a 3-bedroom apartment...         │
│ Bot: What is your budget?                                   │
│ Customer: ₦80 million.                                      │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│ Follow-ups                                                  │
│                                                              │
│ Sep 10 — Call customer — PENDING                            │
└──────────────────────────────────────────────────────────────┘
```

---

# 22. Lead Temperature Display

Temperature should be visually obvious.

```text
HOT
WARM
COLD
```

The visual treatment should be consistent across:

- Dashboard cards
- Lead table
- Lead details
- Notifications

Do not rely solely on color.

Use text labels and/or icons as well for accessibility.

---

# 23. Lead Score

The score should be displayed as:

```text
90 / 100
```

or:

```text
Score: 90
```

Optionally:

```text
█████████░ 90%
```

The exact visualization can be selected during frontend implementation.

---

# 24. Lead Status Control

Sales representatives should be able to update lead status.

Example:

```text
Status
[QUALIFIED ▼]
```

Available valid transitions should be controlled by the backend.

The frontend should not assume that every status is always available.

---

# 25. Conversation Panel

The lead details page should include the conversation history.

Example:

```text
Customer
"Hi, I'm looking for a 3-bedroom apartment in Lekki."

Bot
"What's your budget range?"

Customer
"About ₦80 million."

Bot
"Are you looking to buy within a specific timeframe?"
```

This allows sales representatives to understand the customer's context without asking the same questions again.

---

# 26. Follow-Up Interface

Sales representatives should be able to create follow-ups.

Example:

```text
Create Follow-up

Date: [10 Sep 2026]
Time: [10:00 AM]

Notes:
[Call customer and discuss Lekki properties]

             [Create Follow-up]
```

---

# 27. Follow-Up List

## Route

```text
/follow-ups
```

Example:

```text
┌──────────────────────────────────────────────────────┐
│ Follow-ups                                           │
├──────────────────────────────────────────────────────┤
│ TODAY                                                │
│                                                      │
│ John Doe       Call customer       10:00 AM  PENDING │
│ Mary Jane      Send property list   2:00 PM  PENDING │
│                                                      │
│ UPCOMING                                            │
│                                                      │
│ David Smith    Follow-up            Sep 12           │
└──────────────────────────────────────────────────────┘
```

---

# 28. Notifications

The sales interface should provide notifications for important events.

Examples:

```text
New HOT lead received.

John Doe
3-bedroom apartment
Lekki
₦80M
Score: 90
```

Another:

```text
Follow-up due.

John Doe
Call scheduled for 10:00 AM.
```

---

# 29. Empty States

Empty states should explain what happened.

### No leads

```text
No leads yet.

New customer enquiries will appear here.
```

### No follow-ups

```text
No pending follow-ups.

You're all caught up.
```

### No conversation

```text
No conversation history available.
```

---

# 30. Loading States

Do not display blank screens while data loads.

Use:

- Skeleton loaders
- Spinners for small actions
- Disabled buttons during submission

Example:

```text
Loading leads...
```

For chat:

```text
Assistant is typing...
```

---

# 31. Error States

Errors should be human-readable.

Instead of:

```text
HTTP 502
```

show:

```text
We couldn't load the leads right now.

Please try again.
```

For failed actions:

```text
Unable to update this lead.

Please try again.
```

---

# 32. Responsive Design

The application must support:

```text
Desktop
Tablet
Mobile
```

The customer chat should be designed mobile-first because customers may access the system through their phones.

The sales dashboard should prioritize desktop but remain usable on smaller screens.

---

# 33. Mobile Customer Layout

Example:

```text
┌─────────────────────┐
│ PrimeHomes          │
├─────────────────────┤
│                     │
│ Assistant           │
│                     │
│ ┌─────────────────┐ │
│ │ Hello, how can  │ │
│ │ I help you?     │ │
│ └─────────────────┘ │
│                     │
│      ┌────────────┐ │
│      │ I want to  │ │
│      │ buy a house│ │
│      └────────────┘ │
│                     │
├─────────────────────┤
│ Type message... [➤] │
└─────────────────────┘
```

---

# 34. React Component Architecture

Recommended structure:

```text
frontend/
└── src/
    ├── components/
    │   ├── chat/
    │   │   ├── ChatWindow.jsx
    │   │   ├── MessageBubble.jsx
    │   │   ├── MessageInput.jsx
    │   │   ├── TypingIndicator.jsx
    │   │   └── QuickActions.jsx
    │   │
    │   ├── leads/
    │   │   ├── LeadCard.jsx
    │   │   ├── LeadTable.jsx
    │   │   ├── LeadFilters.jsx
    │   │   ├── LeadDetails.jsx
    │   │   └── LeadStatus.jsx
    │   │
    │   ├── dashboard/
    │   │   ├── StatCard.jsx
    │   │   ├── RecentLeads.jsx
    │   │   └── DashboardSummary.jsx
    │   │
    │   ├── followups/
    │   │   ├── FollowUpForm.jsx
    │   │   └── FollowUpList.jsx
    │   │
    │   └── common/
    │       ├── Button.jsx
    │       ├── Modal.jsx
    │       ├── Badge.jsx
    │       ├── Loading.jsx
    │       └── ErrorMessage.jsx
    │
    ├── pages/
    │   ├── ChatPage.jsx
    │   ├── DashboardPage.jsx
    │   ├── LeadsPage.jsx
    │   ├── LeadDetailsPage.jsx
    │   └── FollowUpsPage.jsx
    │
    ├── services/
    │   └── api.js
    │
    ├── hooks/
    │   ├── useChat.js
    │   ├── useLeads.js
    │   └── useFollowUps.js
    │
    ├── utils/
    │
    ├── App.jsx
    └── main.jsx
```

---

# 35. Frontend State

The React application will need state for:

### Chat

```text
conversationId
messages
isLoading
error
```

### Lead

```text
lead
status
qualification
propertyRequirements
```

### Dashboard

```text
summary
recentLeads
```

### Follow-Ups

```text
followUps
selectedDate
status
```

---

# 36. API Integration

The frontend should communicate through a centralized API service.

Example architecture:

```text
React Component
      ↓
Custom Hook
      ↓
API Service
      ↓
FastAPI
```

For example:

```text
useChat()
    ↓
api.sendMessage()
    ↓
POST /api/v1/chat
```

Components should not contain raw API URLs throughout the application.

---

# 37. Frontend Routes

Initial routes:

```text
/
```

Customer chat.

```text
/dashboard
```

Sales dashboard.

```text
/leads
```

Lead list.

```text
/leads/:id
```

Lead details.

```text
/follow-ups
```

Follow-up management.

---

# 38. Customer Flow

The complete customer journey:

```text
Open Website
     ↓
Chat Welcome
     ↓
Customer Sends Message
     ↓
Bot Understands Intent
     ↓
Bot Collects Missing Information
     ↓
Lead Created/Updated
     ↓
Lead Qualified
     ↓
Customer Receives Confirmation
     ↓
Sales Team Notified
     ↓
Sales Representative Follows Up
```

---

# 39. Sales Representative Flow

```text
Login
  ↓
Dashboard
  ↓
See HOT Lead
  ↓
Open Lead
  ↓
Review Requirements
  ↓
Read Conversation
  ↓
Contact Customer
  ↓
Create Follow-up
  ↓
Update Status
  ↓
Continue Follow-up
  ↓
Convert or Close
```

---

# 40. Important UX Rule

The customer should not need to understand the underlying technology.

The interface should never expose:

```text
AI model
n8n
API
workflow
database
automation
```

The customer sees:

```text
PrimeHomes Assistant
```

The sales team sees:

```text
Lead
Score
Temperature
Status
Conversation
Follow-up
```

The technical complexity stays behind the interface.

---

# 41. Accessibility

The interface should:

- Use readable font sizes.
- Maintain sufficient contrast.
- Support keyboard navigation.
- Use semantic HTML.
- Provide labels for form fields.
- Avoid relying on color alone.
- Provide accessible button labels.
- Make interactive elements sufficiently large on mobile.
- Provide meaningful error messages.

---

# 42. Performance Requirements

The UI should:

- Load quickly.
- Avoid unnecessary API calls.
- Paginate large lead lists.
- Lazy-load where appropriate.
- Avoid rendering thousands of messages at once.
- Show immediate feedback after user actions.

For chat, the user should see a clear loading state immediately after sending a message.

---

# 43. Security Considerations

The frontend must never contain:

- Database credentials
- AI API keys
- n8n credentials
- Internal secrets

Environment variables may contain public frontend configuration, but secrets must remain on the backend.

---

# 44. MVP Screens

The minimum viable frontend should contain:

### Customer

1. Chat page

### Sales

2. Dashboard
3. Lead list
4. Lead details
5. Follow-up management

Everything else can be added incrementally.

---

# 45. MVP Priority

Implementation priority:

```text
Priority 1
Customer Chat
        ↓
Priority 2
Lead List
        ↓
Priority 3
Lead Details
        ↓
Priority 4
Dashboard
        ↓
Priority 5
Follow-ups
```

The customer chat is the most important component because it drives lead generation.

---

# 46. Definition of Done

The UI/UX specification is complete when:

- Customer flow is defined.
- Sales flow is defined.
- Customer chat is defined.
- Dashboard is defined.
- Lead list is defined.
- Lead details are defined.
- Follow-up interface is defined.
- Loading states are defined.
- Error states are defined.
- Empty states are defined.
- Responsive behavior is defined.
- React component structure is defined.
- API integration architecture is defined.
- Accessibility requirements are defined.
- MVP screens are identified.

---

# 47. Next Document

The next document should be:

## n8n Workflow Specification

That document will define exactly how the automation layer works, including:

```text
Customer Message
      ↓
FastAPI
      ↓
n8n Webhook
      ↓
AI Extraction
      ↓
Validation
      ↓
Lead Qualification
      ↓
PostgreSQL
      ↓
Google Sheets
      ↓
Sales Notification
      ↓
Customer Response
```

We will define each n8n workflow, its nodes, inputs, outputs, conditions, error handling and connections before building the workflows in n8n.