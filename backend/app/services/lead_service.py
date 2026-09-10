"""Lead business logic."""

from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.enums import LeadStatus, LeadTemperature
from app.models.lead import Lead, LeadQualification, LeadStatusHistory, PropertyRequirement
from app.models.customer import Customer
from app.schemas.lead import LeadCreate, LeadUpdate
from app.services.scoring_service import score_lead


class LeadService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: LeadCreate) -> Lead:
        lead = Lead(
            customer_id=data.customer_id,
            intent=data.intent,
            transaction_type=data.transaction_type,
            source=data.source,
            status=LeadStatus.NEW,
        )
        self.db.add(lead)
        await self.db.flush()

        if data.property_requirements:
            req = PropertyRequirement(
                lead_id=lead.id,
                **data.property_requirements.model_dump(exclude_unset=True),
            )
            self.db.add(req)

        # Initial status history
        history = LeadStatusHistory(
            lead_id=lead.id,
            old_status=None,
            new_status=LeadStatus.NEW,
            changed_by="SYSTEM",
            reason="Lead created",
        )
        self.db.add(history)

        await self.db.flush()
        await self.db.refresh(lead)
        return lead

    async def get(self, lead_id: UUID) -> Lead | None:
        result = await self.db.execute(
            select(Lead)
            .options(
                selectinload(Lead.customer),
                selectinload(Lead.property_requirement),
                selectinload(Lead.assignments),
            )
            .where(Lead.id == lead_id)
        )
        return result.scalar_one_or_none()

    async def list(
        self,
        *,
        status: LeadStatus | None = None,
        temperature: LeadTemperature | None = None,
        page: int = 1,
        limit: int = 20,
    ) -> tuple[list[Lead], int]:
        query = select(Lead).options(
            selectinload(Lead.customer),
            selectinload(Lead.property_requirement),
        )

        if status:
            query = query.where(Lead.status == status)
        if temperature:
            query = query.where(Lead.temperature == temperature)

        count_q = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_q)).scalar() or 0

        query = query.order_by(Lead.created_at.desc()).offset((page - 1) * limit).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all()), total

    async def update_status(
        self,
        lead: Lead,
        new_status: LeadStatus,
        changed_by: str = "SYSTEM",
        reason: str | None = None,
    ) -> Lead:
        old = lead.status
        lead.status = new_status

        history = LeadStatusHistory(
            lead_id=lead.id,
            old_status=old,
            new_status=new_status,
            changed_by=changed_by,
            reason=reason,
        )
        self.db.add(history)
        await self.db.flush()
        return lead

    async def qualify(self, lead: Lead) -> tuple[Lead, int, LeadTemperature, str]:
        customer = lead.customer
        score, temperature, reason = score_lead(lead, customer)

        lead.score = score
        lead.temperature = temperature

        if lead.status == LeadStatus.NEW and score >= 50:
            await self.update_status(
                lead,
                LeadStatus.QUALIFIED,
                changed_by="SYSTEM",
                reason=f"Auto-qualified (score={score})",
            )

        qualification = LeadQualification(
            lead_id=lead.id,
            score=score,
            temperature=temperature,
            reason=reason,
        )
        self.db.add(qualification)
        await self.db.flush()

        return lead, score, temperature, reason
