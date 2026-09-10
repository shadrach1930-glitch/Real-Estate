# n8n Workflows — PrimeHomes Lead Bot

## Architecture Role

n8n is the **orchestration layer**. It does **not** own business rules or the database.

```text
React → FastAPI → n8n → AI / Sheets / Notifications → FastAPI (callback)
```

FastAPI remains the source of truth for validation, scoring, and persistence.

## Workflow Inventory

| ID     | Name                        | Purpose                                      |
|--------|-----------------------------|----------------------------------------------|
| WF-001 | Receive Customer Message    | Entry point from FastAPI webhook             |
| WF-002 | Process Conversation        | Load context, prepare for AI                 |
| WF-003 | AI Lead Extraction          | Structured extraction (Phase 6)              |
| WF-004 | Validate Lead Data          | Schema + business validation                 |
| WF-005 | Collect Missing Information | Decide next question                         |
| WF-006 | Qualify Lead                | Call FastAPI scoring endpoint                |
| WF-007 | Store Lead                  | Persist via FastAPI                          |
| WF-008 | Google Sheets Sync          | Operational visibility                       |
| WF-009 | Sales Notification          | Alert sales team                             |
| WF-010 | Generate Customer Response  | Natural language reply                       |
| WF-011 | Follow-Up Automation        | Scheduled reminders                          |
| WF-012 | Error Handling              | Centralized failure handling                 |

## WF-001 — Receive Customer Message (Phase 5)

### Trigger

Webhook node:

```text
POST /webhook/primehomes/chat
```

### Expected payload from FastAPI

```json
{
  "request_id": "uuid",
  "conversation_id": "uuid",
  "customer_id": "uuid",
  "message_id": "uuid",
  "message": "I'm looking for a 3-bedroom apartment in Lekki",
  "lead_id": null
}
```

### Recommended nodes (initial)

```text
1. Webhook (POST)
2. Set / Normalize fields
3. IF — required fields present?
4. Respond to Webhook  (immediate ack or final reply)
   └── (Later) Execute Workflow → WF-002
```

### Phase 5 minimal behaviour

For now the workflow can simply:

1. Receive the payload
2. Log / Set fields
3. Return a simple JSON reply so FastAPI can use it:

```json
{
  "reply": "Thanks. I've captured your enquiry. What location and budget range are you working with?",
  "missing_information": ["location", "budget"]
}
```

Later phases will expand this into the full pipeline (AI extraction → validation → qualification → response generation).

## Security

- Set `N8N_WEBHOOK_SECRET` in both FastAPI `.env` and the n8n webhook node (header `X-Webhook-Secret`).
- Prefer production n8n behind authentication + HTTPS.
- Never put AI keys or database credentials in workflow nodes — use n8n Credentials.

## Local Development

```bash
docker compose up -d n8n
```

Open http://localhost:5678  
Default basic auth (from docker-compose): `admin` / `changeme`

Create a webhook workflow with path `primehomes/chat` and activate it.

## Callback to FastAPI

When n8n needs to push results back:

```text
POST http://backend:8000/api/v1/webhooks/n8n
Header: X-Webhook-Secret: <secret>
```

Example body:

```json
{
  "event": "LEAD_PROCESSED",
  "request_id": "...",
  "lead_id": "...",
  "status": "QUALIFIED",
  "score": 85
}
```

## Naming Convention

```text
PRIMEHOMES | WF-001 | Receive Customer Message
PRIMEHOMES | WF-002 | Process Conversation
...
```

See `docs/` (repository history) for the full n8n Workflow Specification.
