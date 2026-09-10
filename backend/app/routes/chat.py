"""
POST /api/v1/chat

Primary customer-facing endpoint.

Flow (Phase 5):
  1. Validate request
  2. Get/create customer + conversation
  3. Store customer message
  4. Trigger n8n workflow (WF-001)
  5. Return reply (from n8n if available, otherwise fallback)
"""

from uuid import uuid4

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db
from app.models.enums import SenderType
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.conversation_service import ConversationService
from app.services.n8n_service import n8n_service

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def send_message(
    body: ChatRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    request_id = request.headers.get("X-Request-ID", str(uuid4()))

    conv_service = ConversationService(db)

    # 1. Customer + Conversation
    customer = await conv_service.get_or_create_customer(body.customer)
    conversation = await conv_service.get_or_create_conversation(
        conversation_id=body.conversation_id,
        customer=customer,
    )

    # 2. Store customer message (source of truth)
    customer_msg = await conv_service.add_message(
        conversation,
        sender_type=SenderType.CUSTOMER,
        content=body.message,
    )

    # 3. Trigger n8n (non-blocking for the lead — we already persisted)
    n8n_result = await n8n_service.trigger_chat_processing(
        request_id=request_id,
        conversation_id=conversation.id,
        customer_id=customer.id,
        message_id=customer_msg.id,
        message=body.message,
        lead_id=conversation.lead_id,
    )

    # 4. Determine reply
    if n8n_result and n8n_result.get("reply"):
        reply_text = n8n_result["reply"]
        lead_id = n8n_result.get("lead_id") or conversation.lead_id
        lead_status = n8n_result.get("lead_status")
        lead_temperature = n8n_result.get("lead_temperature")
        score = n8n_result.get("score")
        missing = n8n_result.get("missing_information", [])
    else:
        # Graceful fallback when n8n is down or not yet configured
        reply_text = (
            "Thanks for your message. I've received your enquiry and our team "
            "will follow up shortly. In the meantime, could you share your "
            "preferred location and approximate budget?"
        )
        lead_id = conversation.lead_id
        lead_status = None
        lead_temperature = None
        score = None
        missing = ["location", "budget"]

    # 5. Store bot reply
    bot_msg = await conv_service.add_message(
        conversation,
        sender_type=SenderType.BOT,
        content=reply_text,
    )

    return ChatResponse(
        conversation_id=conversation.id,
        message_id=bot_msg.id,
        lead_id=lead_id,
        reply=reply_text,
        lead_status=lead_status,
        lead_temperature=lead_temperature,
        score=score,
        missing_information=missing,
    )
