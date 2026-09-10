"""Follow-up endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db
from app.models.enums import FollowUpStatus
from app.models.lead import FollowUp
from app.schemas.followup import FollowUpCreate, FollowUpOut, FollowUpUpdate
from app.services.lead_service import LeadService

router = APIRouter()


@router.post("/leads/{lead_id}/follow-ups", response_model=FollowUpOut, status_code=201)
async def create_follow_up(
    lead_id: UUID,
    body: FollowUpCreate,
    db: AsyncSession = Depends(get_db),
):
    lead_service = LeadService(db)
    lead = await lead_service.get(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    follow_up = FollowUp(
        lead_id=lead_id,
        sales_rep_id=body.sales_rep_id,
        follow_up_date=body.follow_up_date,
        notes=body.notes,
        status=FollowUpStatus.PENDING.value,
    )
    db.add(follow_up)
    await db.flush()
    await db.refresh(follow_up)
    return follow_up


@router.get("/leads/{lead_id}/follow-ups", response_model=list[FollowUpOut])
async def list_follow_ups(
    lead_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(FollowUp)
        .where(FollowUp.lead_id == lead_id)
        .order_by(FollowUp.follow_up_date)
    )
    return list(result.scalars().all())


@router.patch("/follow-ups/{follow_up_id}", response_model=FollowUpOut)
async def update_follow_up(
    follow_up_id: UUID,
    body: FollowUpUpdate,
    db: AsyncSession = Depends(get_db),
):
    from datetime import datetime, timezone

    result = await db.execute(select(FollowUp).where(FollowUp.id == follow_up_id))
    follow_up = result.scalar_one_or_none()
    if not follow_up:
        raise HTTPException(status_code=404, detail="Follow-up not found")

    if body.status:
        follow_up.status = body.status.value
        if body.status == FollowUpStatus.COMPLETED:
            follow_up.completed_at = datetime.now(timezone.utc)

    if body.notes is not None:
        follow_up.notes = body.notes
    if body.follow_up_date is not None:
        follow_up.follow_up_date = body.follow_up_date

    await db.flush()
    return follow_up
