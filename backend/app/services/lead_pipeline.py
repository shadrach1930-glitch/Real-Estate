"""
Lead processing pipeline.

Orchestrates:
  AI extraction → validation → create/update lead → score → audit → sheets sync
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
from app.services.sheets_service import sheets_service
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
        lead = await self._get_or_create_lead(customer, conversation, extraction)
        await self._apply_extraction(lead, extraction, customer)

        await self.db.refresh(lead, attribute_names=["property_requirement", "customer"])
        lead, score, temperature, reason = await self.lead_service.qualify(lead)

        await self._store_ai_audit(
            lead_id=lead.id,
            message_id=message_id,
            extraction=extraction,
        )

        if conversation.lead_id != lead.id:
            conversation.lead_id = lead.id
            await self.db.flush()

        # Fire-and-forget sheets sync (never blocks the customer response)
        await self._sync_to_sheets(lead, customer)

        return lead, score, temperature.value if temperature else None, reason

    async def _get_or_create_lead(
        self,
        customer: Customer,
        conversation: Conversation,
        extraction: LeadExtraction,
    ) -> Lead:
        if conversation.lead_id:
            lead = await self.lead_service.get(conversation.lead_id)
            if lead:
                return lead

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

        lead = Lead(
            customer_id=customer.id,
            intent=extraction.intent,
            transaction_type=extraction.transaction_type,
            status=LeadStatus.NEW,
            source="WEB_CHAT",
        )
        self.db.add(lead)
        await self.db.flush()

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
        if extraction.intent and extraction.intent != Intent.OTHER:
            lead.intent = extraction.intent
        if extraction.transaction_type and extraction.transaction_type != TransactionType.UNKNOWN:
            lead.transaction_type = extraction.transaction_type

        if extraction.customer:
            if extraction.customer.name and not customer.name:
                customer.name = extraction.customer.name
            if extraction.customer.email and not customer.email:
                customer.email = extraction.customer.email
            if extraction.customer.phone and not customer.phone:
                customer.phone = extraction.customer.phone

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

    async def _sync_to_sheets(self, lead: Lead, customer: Customer) -> None:
        req = lead.property_requirement
        data = {
            "id": str(lead.id),
            "customer_name": customer.name,
            "phone": customer.phone,
            "email": customer.email,
            "property_type": req.property_type.value if req and req.property_type else None,
            "location": req.location if req else None,
            "budget": float(req.budget_max) if req and req.budget_max is not None else None,
            "score": lead.score,
            "temperature": lead.temperature.value if lead.temperature else None,
            "status": lead.status.value if lead.status else None,
            "created_at": lead.created_at.isoformat() if lead.created_at else None,
        }
        try:
            await sheets_service.sync_lead(data)
        except Exception:
            pass  # never break the main flow
