"""Lead-related schemas."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import (
    Intent,
    LeadStatus,
    LeadTemperature,
    PropertyType,
    Timeline,
    TransactionType,
)
from app.schemas.customer import CustomerOut


class PropertyRequirementBase(BaseModel):
    property_type: PropertyType | None = None
    bedrooms: int | None = Field(None, ge=0, le=50)
    location: str | None = Field(None, max_length=150)
    budget_min: Decimal | None = Field(None, ge=0)
    budget_max: Decimal | None = Field(None, ge=0)
    currency: str = "NGN"
    additional_requirements: str | None = None
    timeline: Timeline | None = None


class PropertyRequirementOut(PropertyRequirementBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    lead_id: UUID
    created_at: datetime
    updated_at: datetime


class LeadCreate(BaseModel):
    customer_id: UUID
    intent: Intent = Intent.OTHER
    transaction_type: TransactionType | None = None
    property_requirements: PropertyRequirementBase | None = None
    source: str | None = None


class LeadUpdate(BaseModel):
    status: LeadStatus | None = None
    intent: Intent | None = None
    transaction_type: TransactionType | None = None
    notes: str | None = None


class LeadAssign(BaseModel):
    sales_rep_id: UUID


class LeadOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    customer_id: UUID
    intent: Intent
    transaction_type: TransactionType | None
    status: LeadStatus
    score: int | None
    temperature: LeadTemperature | None
    source: str | None
    created_at: datetime
    updated_at: datetime


class LeadDetailOut(LeadOut):
    customer: CustomerOut | None = None
    property_requirements: PropertyRequirementOut | None = None
    assigned_sales_rep: dict | None = None


class LeadListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    customer_name: str | None = None
    property_type: PropertyType | None = None
    location: str | None = None
    budget: Decimal | None = None
    temperature: LeadTemperature | None = None
    status: LeadStatus
    score: int | None = None
    created_at: datetime


class QualifyResponse(BaseModel):
    lead_id: UUID
    score: int
    temperature: LeadTemperature
    reason: str


class StatusHistoryItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    type: str = "STATUS_CHANGE"
    old_status: LeadStatus | None
    new_status: LeadStatus
    created_at: datetime
    reason: str | None = None


class LeadHistoryOut(BaseModel):
    lead_id: UUID
    events: list[StatusHistoryItem]
