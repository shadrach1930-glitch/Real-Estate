"""
Lead processing pipeline.

Orchestrates:
  AI extraction → validation → create/update lead → score → audit

Principle: AI interprets. Backend validates & decides. Database stores.
"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.conversation import AIExtraction, Conversation
from app.models.customer import Customer
from app.models.enums import Intent, LeadStatus, TransactionType
from app.models.lead import Lead, PropertyRequirement
from app.schemas.ai import LeadExtraction
from app.services.ai.prompts import PROMPT_VERSIONS
from app.services.lead_service import LeadService
from app.services.scoring_service import score_lead
from app.config import settings


class LeadPipeline:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.lead_service = LeadService(db)

    async def process_extraction(
        self,
        *,
        extraction: LeadExtraction,
        customer: Customer,
        conversation: Conversation,
        message_id: UUID,
    ) -> tuple[Lead, int | None, str | None, str]:
        """
        Apply a validated extraction to the database.

        Returns: (lead, score, temperature, reply_hint)
        """
        # 1. Find or create lead for this conversation/customer
        lead = await self._get_or_create_lead(customer, conversation, extraction)

        # 2. Merge extraction into lead + property requirements
        await self._apply_extraction(lead, extraction, customer)

        # 3. Score
        await self.db.refresh(lead, attribute_names=["property_requirement", "customer"])
        lead, score, temperature, reason = await self.lead_service.qualify(lead)

        # 4. Audit AI extraction
        await self._store_ai_audit(
            lead_id=lead.id,
            message_id=message_id,
            extraction=extraction,
        )

        # 5. Link conversation → lead
        if conversation.lead_id != lead.id:
            conversation.lead_id = lead.id
            await self.db.flush()

        return lead, score, temperature.value if temperature else None, reason

    async def _get_or_create_lead(
        self,
        customer: Customer,
        conversation: Conversation,
        extraction: LeadExtraction,
    ) -> Lead:
        # Prefer existing lead linked to conversation
        if conversation.lead_id:
            lead = await self.lead_service.get(conversation.lead_id)
            if lead:
                return lead

        # Otherwise look for an open lead for this customer
        result = await self.db.execute(
            select(Lead)
            .options(selectinload(Lead.property_requirement))
            .where(
                Lead.customer_id == customer.id,
                Lead.status.in_([
                    LeadStatus.NEW,
                    LeadStatus.QUALIFIED,
                    LeadStatus.ASSIGNED,
                    LeadStatus.CONTACTED,
                    LeadStatus.FOLLOW_UP,
                ]),
            )
            .order_by(Lead.created_at.desc())
            .limit(1)
        )
        existing = result.scalar_one_or_none()
        if existing:
            return existing

        # Create new lead
        lead = Lead(
            customer_id=customer.id,
            intent=extraction.intent,
            transaction_type=extraction.transaction_type,
            status=LeadStatus.NEW,
            source="WEB_CHAT",
        )
        self.db.add(lead)
        await self.db.flush()

        # Initial property requirement row
        req = PropertyRequirement(lead_id=lead.id, currency="NGN")
        self.db.add(req)
        await self.db.flush()

        return lead

    async def _apply_extraction(
        self,
        lead: Lead,
        extraction: LeadExtraction,
        customer: Customer,
    ) -> None:
        """Merge non-null extraction fields into lead & customer (never invent)."""

        # Intent / transaction
        if extraction.intent and extraction.intent != Intent.OTHER:
            lead.intent = extraction.intent
        if extraction.transaction_type and extraction.transaction_type != TransactionType.UNKNOWN:
            lead.transaction_type = extraction.transaction_type

        # Customer contact (only fill gaps)
        if extraction.customer:
            if extraction.customer.name and not customer.name:
                customer.name = extraction.customer.name
            if extraction.customer.email and not customer.email:
                customer.email = extraction.customer.email
            if extraction.customer.phone and not customer.phone:
                customer.phone = extraction.customer.phone

        # Property requirements
        req = lead.property_requirement
        if not req:
            req = PropertyRequirement(lead_id=lead.id, currency="NGN")
            self.db.add(req)
            lead.property_requirement = req

        if extraction.property_type:
            req.property_type = extraction.property_type
        if extraction.bedrooms is not None:
            req.bedrooms = extraction.bedrooms
        if extraction.location:
            req.location = extraction.location
        if extraction.budget_min is not None:
            req.budget_min = extraction.budget_min
        if extraction.budget_max is not None:
            req.budget_max = extraction.budget_max
        if extraction.currency:
            req.currency = extraction.currency
        if extraction.timeline:
            req.timeline = extraction.timeline
        if extraction.additional_requirements:
            existing = req.additional_requirements or ""
            new = "; ".join(extraction.additional_requirements)
            req.additional_requirements = f"{existing}; {new}".strip("; ") if existing else new

        await self.db.flush()

    async def _store_ai_audit(
        self,
        *,
        lead_id: UUID,
        message_id: UUID,
        extraction: LeadExtraction,
    ) -> None:
        record = AIExtraction(
            lead_id=lead_id,
            message_id=message_id,
            model=settings.ai_model or "fallback-rules",
            prompt_version=PROMPT_VERSIONS.get("extraction", "lead-extraction-v1.0"),
            extracted_data=extraction.model_dump(mode="json"),
            confidence=extraction.confidence.overall if extraction.confidence else None,
        )
        self.db.add(record)
        await self.db.flush()
