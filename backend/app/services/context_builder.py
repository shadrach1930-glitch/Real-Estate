"""
Conversation context builder.

Assembles the information the AI (and reply generator) need:
  - Recent messages
  - Existing structured lead data
  - Customer profile
"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.conversation import Conversation, Message
from app.models.customer import Customer
from app.models.lead import Lead


class ContextBuilder:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def build(
        self,
        *,
        conversation: Conversation,
        customer: Customer,
        limit_messages: int = 8,
    ) -> dict:
        """Return a context dict safe to pass to the AI and reply logic."""

        # Recent messages (excluding the one just added if needed)
        result = await self.db.execute(
            select(Message)
            .where(Message.conversation_id == conversation.id)
            .order_by(Message.created_at.desc())
            .limit(limit_messages)
        )
        messages = list(reversed(result.scalars().all()))

        conversation_text = "\n".join(
            f"{m.sender_type.value}: {m.content}" for m in messages
        )

        # Existing lead snapshot
        existing_lead = None
        lead = None
        if conversation.lead_id:
            lead_result = await self.db.execute(
                select(Lead)
                .options(selectinload(Lead.property_requirement))
                .where(Lead.id == conversation.lead_id)
            )
            lead = lead_result.scalar_one_or_none()

        if lead:
            req = lead.property_requirement
            existing_lead = {
                "intent": lead.intent.value if lead.intent else None,
                "transaction_type": lead.transaction_type.value if lead.transaction_type else None,
                "status": lead.status.value if lead.status else None,
                "score": lead.score,
                "temperature": lead.temperature.value if lead.temperature else None,
                "property_type": req.property_type.value if req and req.property_type else None,
                "bedrooms": req.bedrooms if req else None,
                "location": req.location if req else None,
                "budget_min": float(req.budget_min) if req and req.budget_min is not None else None,
                "budget_max": float(req.budget_max) if req and req.budget_max is not None else None,
                "currency": req.currency if req else "NGN",
                "timeline": req.timeline.value if req and req.timeline else None,
            }

        customer_info = {
            "name": customer.name,
            "email": customer.email,
            "phone": customer.phone,
        }

        return {
            "conversation_text": conversation_text,
            "existing_lead": existing_lead,
            "customer": customer_info,
            "lead": lead,
        }
