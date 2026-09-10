# n8n Workflows

This directory will contain the exported / documented n8n workflows for the PrimeHomes Lead Bot.

## Workflow Inventory (from Specification)

| ID     | Name                          | Purpose                              |
|--------|-------------------------------|--------------------------------------|
| WF-001 | Receive Customer Message      | Entry point from FastAPI             |
| WF-002 | Process Conversation          | Context building                     |
| WF-003 | AI Lead Extraction            | Structured extraction                |
| WF-004 | Validate Lead Data            | Schema + business validation         |
| WF-005 | Collect Missing Information   | Progressive questioning logic        |
| WF-006 | Qualify Lead                  | Scoring + temperature                |
| WF-007 | Store Lead                    | Persistence via FastAPI              |
| WF-008 | Google Sheets Sync            | Operational visibility               |
| WF-009 | Sales Notification            | Alert sales team                     |
| WF-010 | Generate Customer Response    | Natural language reply               |
| WF-011 | Follow-Up Automation          | Scheduled follow-up reminders        |
| WF-012 | Error Handling                | Centralized failure handling         |

Workflows will be added as JSON exports or documentation in later phases.

See `docs/n8n Workflow Specification.md` for full details.
