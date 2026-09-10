from app.schemas.chat import ChatRequest, ChatResponse, ConversationOut, MessageOut
from app.schemas.common import ErrorDetail, ErrorResponse, PaginatedResponse
from app.schemas.customer import CustomerCreate, CustomerOut, CustomerUpdate
from app.schemas.dashboard import DashboardSummary
from app.schemas.followup import FollowUpCreate, FollowUpOut, FollowUpUpdate
from app.schemas.lead import (
    LeadAssign,
    LeadCreate,
    LeadDetailOut,
    LeadHistoryOut,
    LeadListItem,
    LeadOut,
    LeadUpdate,
    PropertyRequirementOut,
    QualifyResponse,
)

__all__ = [
    "ChatRequest",
    "ChatResponse",
    "ConversationOut",
    "MessageOut",
    "ErrorDetail",
    "ErrorResponse",
    "PaginatedResponse",
    "CustomerCreate",
    "CustomerOut",
    "CustomerUpdate",
    "DashboardSummary",
    "FollowUpCreate",
    "FollowUpOut",
    "FollowUpUpdate",
    "LeadAssign",
    "LeadCreate",
    "LeadDetailOut",
    "LeadHistoryOut",
    "LeadListItem",
    "LeadOut",
    "LeadUpdate",
    "PropertyRequirementOut",
    "QualifyResponse",
]
