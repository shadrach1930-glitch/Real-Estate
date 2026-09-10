"""
POST /api/v1/chat

Full pipeline with conversation context:
  1. Store customer message
  2. Build context (history + existing lead)
  3. AI extraction (context-aware)
  4. Persist / update Lead + score
  5. Trigger n8n
  6. Context-aware progressive reply
"""

from uuid import uuid4

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db
from app.models.enums import LeadTemperature, SenderType
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.ai import ai_extractor, AIExtractionError
from app.services.context_builder import ContextBuilder
from app.services.conversation_service import ConversationService
from app.services.lead_pipeline import LeadPipeline
from app.services.n8n_service import n8n_service
from app.services.reply_service import build_reply

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def send_message(
    body: ChatRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    request_id = request.headers.get("X-Request-ID", str(uuid4()))

    conv_service = ConversationService(db)
    context_builder = ContextBuilder(db)
    pipeline = LeadPipeline(db)

    # 1. Customer + Conversation
    customer = await conv_service.get_or_create_customer(body.customer)
    conversation = await conv_service.get_or_create_conversation(
        conversation_id=body.conversation_id,
        customer=customer,
    )

    # 2. Store customer message
    customer_msg = await conv_service.add_message(
        conversation,
        sender_type=SenderType.CUSTOMER,
        content=body.message,
    )

    # 3. Build context from history + existing lead
    ctx = await context_builder.build(
        conversation=conversation,
        customer=customer,
    )

    # 4. AI Extraction (with context)
    extraction = None
    try:
        extraction = await ai_extractor.extract(
            customer_message=body.message,
            conversation_context=ctx["conversation_text"],
            existing_lead=ctx["existing_lead"],
        )
    except AIExtractionError:
        pass

    # 5. Persist + qualify
    lead = None
    score = None
    temperature = None

    if extraction:
        lead, score, temperature, _ = await pipeline.process_extraction(
            extraction=extraction,
            customer=customer,
            conversation=conversation,
            message_id=customer_msg.id,
        )

    # 6. n8n (async side-effects)
    await n8n_service.trigger_chat_processing(
        request_id=request_id,
        conversation_id=conversation.id,
        customer_id=customer.id,
        message_id=customer_msg.id,
        message=body.message,
        lead_id=lead.id if lead else conversation.lead_id,
    )

    # 7. Progressive, context-aware reply
    if extraction:
        reply_text = build_reply(
            extraction,
            score=score,
            temperature=temperature,
            customer_name=customer.name,
        )
        missing = extraction.missing_information
    else:
        reply_text = (
            "Thanks for your message. I've received your enquiry. "
            "Could you tell me your preferred location and budget range?"
        )
        missing = ["location", "budget"]

    # 8. Store bot reply
    bot_msg = await conv_service.add_message(
        conversation,
        sender_type=SenderType.BOT,
        content=reply_text,
    )

    return ChatResponse(
        conversation_id=conversation.id,
        message_id=bot_msg.id,
        lead_id=lead.id if lead else None,
        reply=reply_text,
        lead_status=lead.status if lead else None,
        lead_temperature=LeadTemperature(temperature) if temperature else None,
        score=score,
        missing_information=missing or [],
    )
