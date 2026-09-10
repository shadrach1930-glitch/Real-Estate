"""
Export all models so Alembic and the application can discover them.
"""

from app.models.customer import Customer
from app.models.lead import (
    FollowUp,
    Lead,
    LeadAssignment,
    LeadQualification,
    LeadStatusHistory,
    PropertyRequirement,
    SalesRep,
)
from app.models.conversation import AIExtraction, Conversation, Message
from app.models.enums import (
    Channel,
    FollowUpStatus,
    Intent,
    LeadStatus,
    LeadTemperature,
    PropertyType,
    SenderType,
    Timeline,
    TransactionType,
)

__all__ = [
    "Customer",
    "Lead",
    "PropertyRequirement",
    "LeadQualification",
    "SalesRep",
    "LeadAssignment",
    "LeadStatusHistory",
    "FollowUp",
    "Conversation",
    "Message",
    "AIExtraction",
    "Intent",
    "TransactionType",
    "PropertyType",
    "Timeline",
    "LeadStatus",
    "LeadTemperature",
    "Channel",
    "SenderType",
    "FollowUpStatus",
]
