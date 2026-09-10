"""Follow-up schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import FollowUpStatus


class FollowUpCreate(BaseModel):
    sales_rep_id: UUID | None = None
    follow_up_date: datetime
    notes: str | None = None


class FollowUpUpdate(BaseModel):
    status: FollowUpStatus | None = None
    notes: str | None = None
    follow_up_date: datetime | None = None


class FollowUpOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    lead_id: UUID
    sales_rep_id: UUID | None
    follow_up_date: datetime
    notes: str | None
    status: str
    completed_at: datetime | None
    created_at: datetime
