"""n8n → FastAPI webhook receiver."""

import logging
from typing import Any

from fastapi import APIRouter, Header, HTTPException, Request
from pydantic import BaseModel, Field

from app.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


class N8nEvent(BaseModel):
    event: str = Field(..., examples=["LEAD_PROCESSED", "LEAD_QUALIFIED", "ERROR"])
    request_id: str | None = None
    conversation_id: str | None = None
    lead_id: str | None = None
    status: str | None = None
    score: int | None = None
    temperature: str | None = None
    data: dict[str, Any] | None = None


@router.post("/webhooks/n8n")
async def n8n_webhook(
    body: N8nEvent,
    request: Request,
    x_webhook_secret: str | None = Header(None, alias="X-Webhook-Secret"),
):
    """
    Receive events from n8n back into the backend.

    In production this endpoint must be protected.
    """
    # Simple shared-secret check (expand later with HMAC if needed)
    if settings.n8n_webhook_secret and x_webhook_secret != settings.n8n_webhook_secret:
        raise HTTPException(status_code=401, detail="Invalid webhook secret")

    logger.info(
        "n8n event received: event=%s request_id=%s lead_id=%s",
        body.event,
        body.request_id,
        body.lead_id,
    )

    # Future: update lead status, store AI extraction audit, etc.
    # For now we acknowledge receipt so n8n can continue.

    return {
        "received": True,
        "event": body.event,
        "request_id": body.request_id,
    }
