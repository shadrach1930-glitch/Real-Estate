"""Lead endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db
from app.models.enums import LeadStatus, LeadTemperature
from app.schemas.common import PaginatedResponse
from app.schemas.lead import (
    LeadCreate,
    LeadDetailOut,
    LeadHistoryOut,
    LeadListItem,
    LeadOut,
    LeadUpdate,
    QualifyResponse,
    StatusHistoryItem,
)
from app.services.lead_service import LeadService

router = APIRouter()


@router.post("/leads", response_model=LeadOut, status_code=201)
async def create_lead(
    body: LeadCreate,
    db: AsyncSession = Depends(get_db),
):
    service = LeadService(db)
    lead = await service.create(body)
    return lead


@router.get("/leads", response_model=PaginatedResponse[LeadListItem])
async def list_leads(
    status: LeadStatus | None = None,
    temperature: LeadTemperature | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    service = LeadService(db)
    leads, total = await service.list(
        status=status, temperature=temperature, page=page, limit=limit
    )

    items = []
    for lead in leads:
        req = lead.property_requirement
        items.append(
            LeadListItem(
                id=lead.id,
                customer_name=lead.customer.name if lead.customer else None,
                property_type=req.property_type if req else None,
                location=req.location if req else None,
                budget=req.budget_max if req else None,
                temperature=lead.temperature,
                status=lead.status,
                score=lead.score,
                created_at=lead.created_at,
            )
        )

    return PaginatedResponse(items=items, page=page, limit=limit, total=total)


@router.get("/leads/{lead_id}", response_model=LeadDetailOut)
async def get_lead(
    lead_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    service = LeadService(db)
    lead = await service.get(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@router.patch("/leads/{lead_id}", response_model=LeadOut)
async def update_lead(
    lead_id: UUID,
    body: LeadUpdate,
    db: AsyncSession = Depends(get_db),
):
    service = LeadService(db)
    lead = await service.get(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    if body.status and body.status != lead.status:
        await service.update_status(
            lead,
            body.status,
            changed_by="API",
            reason=body.notes,
        )

    if body.intent:
        lead.intent = body.intent
    if body.transaction_type:
        lead.transaction_type = body.transaction_type

    await db.flush()
    return lead


@router.post("/leads/{lead_id}/qualify", response_model=QualifyResponse)
async def qualify_lead(
    lead_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    service = LeadService(db)
    lead = await service.get(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    lead, score, temperature, reason = await service.qualify(lead)

    return QualifyResponse(
        lead_id=lead.id,
        score=score,
        temperature=temperature,
        reason=reason,
    )


@router.get("/leads/{lead_id}/history", response_model=LeadHistoryOut)
async def lead_history(
    lead_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    from sqlalchemy import select
    from app.models.lead import LeadStatusHistory

    service = LeadService(db)
    lead = await service.get(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    result = await db.execute(
        select(LeadStatusHistory)
        .where(LeadStatusHistory.lead_id == lead_id)
        .order_by(LeadStatusHistory.created_at)
    )
    history = result.scalars().all()

    events = [
        StatusHistoryItem(
            old_status=h.old_status,
            new_status=h.new_status,
            created_at=h.created_at,
            reason=h.reason,
        )
        for h in history
    ]

    return LeadHistoryOut(lead_id=lead_id, events=events)
