"""Chat and conversation schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import LeadStatus, LeadTemperature, SenderType
from app.schemas.customer import CustomerCreate


class ChatRequest(BaseModel):
    conversation_id: UUID | None = None
    message: str = Field(..., min_length=1, max_length=4000)
    customer: CustomerCreate | None = None


class ChatResponse(BaseModel):
    conversation_id: UUID
    message_id: UUID
    lead_id: UUID | None = None
    reply: str
    lead_status: LeadStatus | None = None
    lead_temperature: LeadTemperature | None = None
    score: int | None = None
    missing_information: list[str] = []


class MessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    sender_type: SenderType
    content: str
    created_at: datetime


class ConversationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    customer_id: UUID
    lead_id: UUID | None
    channel: str
    messages: list[MessageOut] = []
    created_at: datetime
    updated_at: datetime
