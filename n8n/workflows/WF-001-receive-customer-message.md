# WF-001 — Receive Customer Message

**Status:** Phase 5 skeleton  
**Trigger:** Webhook  
**Path:** `/webhook/primehomes/chat`

## Purpose

Entry point for every customer message coming from FastAPI.

## Input

```json
{
  "request_id": "string",
  "conversation_id": "uuid",
  "customer_id": "uuid",
  "message_id": "uuid",
  "message": "string",
  "lead_id": "uuid | null"
}
```

## Processing (Phase 5)

1. Validate required fields exist (`message`, `conversation_id`, `request_id`).
2. Optionally check idempotency (same `message_id` already processed).
3. Return a structured response that FastAPI can use immediately.

## Output (returned to FastAPI)

```json
{
  "reply": "Thanks for your message. I've received your enquiry...",
  "missing_information": ["location", "budget"],
  "lead_id": null,
  "lead_status": null,
  "score": null
}
```

## Future expansion (Phase 6+)

```text
Webhook
  → Set fields
  → Execute Workflow: WF-002 (Process Conversation)
  → Execute Workflow: WF-003 (AI Extraction)
  → Execute Workflow: WF-004 (Validate)
  → Execute Workflow: WF-006 (Qualify via FastAPI)
  → Execute Workflow: WF-010 (Generate Response)
  → Respond to Webhook
```

## Error path

On failure → Execute WF-012 (Error Handling) and still return a safe fallback reply so the customer is never left without a response.
