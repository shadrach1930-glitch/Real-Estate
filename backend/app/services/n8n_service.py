"""
n8n integration service.

FastAPI triggers n8n workflows via webhook.
n8n is responsible for orchestration (AI, Sheets, notifications).
"""

import logging
from typing import Any
from uuid import UUID

import httpx

from app.config import settings

logger = logging.getLogger(__name__)


class N8nService:
    def __init__(self):
        self.base_url = settings.n8n_base_url.rstrip("/")
        self.webhook_url = settings.n8n_webhook_url
        self.secret = settings.n8n_webhook_secret

    async def trigger_chat_processing(
        self,
        *,
        request_id: str,
        conversation_id: UUID,
        customer_id: UUID,
        message_id: UUID,
        message: str,
        lead_id: UUID | None = None,
    ) -> dict[str, Any] | None:
        """
        Trigger WF-001 / Process Conversation workflow.

        Returns the n8n response body on success, or None on failure.
        Failures are logged but do not raise — the lead must not be lost
        just because n8n is temporarily unavailable.
        """
        payload = {
            "request_id": request_id,
            "conversation_id": str(conversation_id),
            "customer_id": str(customer_id),
            "message_id": str(message_id),
            "message": message,
            "lead_id": str(lead_id) if lead_id else None,
        }

        headers = {
            "Content-Type": "application/json",
            "X-Request-ID": request_id,
        }
        if self.secret:
            headers["X-Webhook-Secret"] = self.secret

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.webhook_url,
                    json=payload,
                    headers=headers,
                )

                if response.status_code >= 400:
                    logger.warning(
                        "n8n webhook returned %s: %s",
                        response.status_code,
                        response.text[:500],
                    )
                    return None

                # n8n may return the generated reply or just an ack
                try:
                    return response.json()
                except Exception:
                    return {"status": "accepted"}

        except httpx.TimeoutException:
            logger.error("n8n webhook timed out (request_id=%s)", request_id)
            return None
        except httpx.RequestError as exc:
            logger.error(
                "n8n webhook request failed (request_id=%s): %s",
                request_id,
                exc,
            )
            return None


n8n_service = N8nService()
