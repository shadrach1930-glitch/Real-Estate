"""
POST /api/v1/chat

Primary customer-facing endpoint.
For the current phase this stores the message and returns a placeholder reply.
Full AI + n8n pipeline will be wired in later phases.
"""

from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db
from app.models.enums import SenderType
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.conversation_service import ConversationService

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def send_message(
    body: ChatRequest,
    db: AsyncSession = Depends(get_db),
):
    conv_service = ConversationService(db)

    customer = await conv_service.get_or_create_customer(body.customer)
    conversation = await conv_service.get_or_create_conversation(
        conversation_id=body.conversation_id,
        customer=customer,
    )

    # Store customer message
    customer_msg = await conv_service.add_message(
        conversation,
        sender_type=SenderType.CUSTOMER,
        content=body.message,
    )

    # Placeholder reply (AI pipeline comes in Phase 6+)
    reply_text = (
        "Thanks for your message. I've received your enquiry. "
        "Our full AI assistant will be connected shortly. "
        "In the meantime, could you tell me your preferred location and budget range?"
    )

    bot_msg = await conv_service.add_message(
        conversation,
        sender_type=SenderType.BOT,
        content=reply_text,
    )

    return ChatResponse(
        conversation_id=conversation.id,
        message_id=bot_msg.id,
        lead_id=conversation.lead_id,
        reply=reply_text,
        missing_information=["location", "budget"],
    )
