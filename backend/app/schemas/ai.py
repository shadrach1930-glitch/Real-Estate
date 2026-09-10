"""AI extraction schemas — matches AI & Prompt Engineering Specification."""

from decimal import Decimal
from typing import Any

from pydantic import BaseModel, Field, field_validator

from app.models.enums import Intent, PropertyType, Timeline, TransactionType


class CustomerInfo(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None


class ConfidenceScores(BaseModel):
    overall: float = Field(0.0, ge=0.0, le=1.0)
    intent: float = Field(0.0, ge=0.0, le=1.0)
    property_type: float = Field(0.0, ge=0.0, le=1.0)
    bedrooms: float = Field(0.0, ge=0.0, le=1.0)
    location: float = Field(0.0, ge=0.0, le=1.0)
    budget: float = Field(0.0, ge=0.0, le=1.0)
    timeline: float = Field(0.0, ge=0.0, le=1.0)


class LeadExtraction(BaseModel):
    """Structured output required from the AI extraction operation."""

    intent: Intent = Intent.OTHER
    transaction_type: TransactionType | None = None
    property_type: PropertyType | None = None
    bedrooms: int | None = Field(None, ge=0, le=50)
    location: str | None = None
    budget_min: Decimal | None = Field(None, ge=0)
    budget_max: Decimal | None = Field(None, ge=0)
    currency: str = "NGN"
    timeline: Timeline | None = None
    customer: CustomerInfo = Field(default_factory=CustomerInfo)
    additional_requirements: list[str] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)
    confidence: ConfidenceScores = Field(default_factory=ConfidenceScores)

    @field_validator("currency", mode="before")
    @classmethod
    def normalize_currency(cls, v: Any) -> str:
        if not v:
            return "NGN"
        v = str(v).upper().strip()
        if v in ("NAIRA", "₦", "N", "NGN"):
            return "NGN"
        return v
