"""Dashboard summary endpoint."""

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db
from app.models.enums import LeadStatus, LeadTemperature
from app.models.lead import FollowUp, Lead
from app.schemas.dashboard import DashboardSummary

router = APIRouter()


@router.get("/dashboard/summary", response_model=DashboardSummary)
async def dashboard_summary(db: AsyncSession = Depends(get_db)):
    async def count(condition=None):
        q = select(func.count()).select_from(Lead)
        if condition is not None:
            q = q.where(condition)
        return (await db.execute(q)).scalar() or 0

    total = await count()
    new = await count(Lead.status == LeadStatus.NEW)
    hot = await count(Lead.temperature == LeadTemperature.HOT)
    warm = await count(Lead.temperature == LeadTemperature.WARM)
    cold = await count(Lead.temperature == LeadTemperature.COLD)
    qualified = await count(Lead.status == LeadStatus.QUALIFIED)
    converted = await count(Lead.status == LeadStatus.CONVERTED)

    pending_q = select(func.count()).select_from(FollowUp).where(
        FollowUp.status == "PENDING"
    )
    pending = (await db.execute(pending_q)).scalar() or 0

    return DashboardSummary(
        total_leads=total,
        new_leads=new,
        hot_leads=hot,
        warm_leads=warm,
        cold_leads=cold,
        qualified_leads=qualified,
        converted_leads=converted,
        pending_follow_ups=pending,
    )
