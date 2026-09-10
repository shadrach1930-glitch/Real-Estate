"""n8n webhook receiver."""

from fastapi import APIRouter, Request
from pydantic import BaseModel

router = APIRouter()


class N8nEvent(BaseModel):
    event: str
    lead_id: str | None = None
    status: str | None = None
    score: int | None = None


@router.post("/webhooks/n8n")
async def n8n_webhook(body: N8nEvent, request: Request):
    """
    Receive events from n8n.
    Protected in production via webhook secret / signature.
    """
    # TODO: verify N8N_WEBHOOK_SECRET header when configured
    return {"received": True, "event": body.event}
