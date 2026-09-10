"""
POST /api/v1/chat

Full pipeline (Phase 7/8):
  1. Store customer message
  2. AI extraction
  3. Persist / update Lead + score
  4. Trigger n8n
  5. Return contextual reply
"""

from uuid import uuid4

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db
from app.models.enums import Intent, LeadStatus, LeadTemperature, SenderType
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.ai import ai_extractor, AIExtractionError
from app.services.conversation_service import ConversationService
from app.services.lead_pipeline import LeadPipeline
from app.services.n8n_service import n8n_service

router = APIRouter()


def _build_reply(extraction, score: int | None = None, temperature: str | None = None) -> str:
    """Contextual reply based on extraction + qualification state."""
    intent = extraction.intent

    if intent == Intent.HUMAN_REQUEST:
        return (
            "Absolutely. I'll connect you with a PrimeHomes representative. "
            "Could you please share your name and phone number so they can reach you?"
        )

    # Acknowledge what we captured
    bits = []
    if extraction.bedrooms:
        bits.append(f"{extraction.bedrooms}-bedroom")
    if extraction.property_type:
        bits.append(extraction.property_type.value.lower())
    if extraction.location:
        bits.append(f"in {extraction.location}")
    if extraction.budget_max:
        bits.append(f"with a budget up to ₦{extraction.budget_max:,.0f}")

    ack = ""
    if bits:
        ack = f"I've noted you're looking for a {' '.join(bits)}. "

    missing = extraction.missing_information or []

    # High-value leads get a stronger close
    if temperature == "HOT" or (score is not None and score >= 80):
        return (
            f"{ack}Thanks — your requirements look clear. "
            "A member of our sales team will follow up with you shortly. "
            "Could you confirm the best phone number to reach you on?"
        )

    # Progressive questions
    if "location" in missing:
        return f"{ack}Which location are you interested in?"
    if "budget" in missing:
        return f"{ack}What budget range are you working with?"
    if "property_type" in missing:
        return f"{ack}What type of property are you looking for (apartment, house, duplex, or land)?"
    if "timeline" in missing:
        return f"{ack}When are you looking to buy or rent?"
    if "phone" in missing or "name" in missing:
        return f"{ack}Could you share your name and a phone number so our team can follow up?"

    return (
        f"{ack}Thanks, I've captured your requirements. "
        "A member of our sales team will follow up with you shortly."
    )


@router.post("/chat", response_model=ChatResponse)
async def send_message(
    body: ChatRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    request_id = request.headers.get("X-Request-ID", str(uuid4()))

    conv_service = ConversationService(db)
    pipeline = LeadPipeline(db)

    # 1. Customer + Conversation
    customer = await conv_service.get_or_create_customer(body.customer)
    conversation = await conv_service.get_or_create_conversation(
        conversation_id=body.conversation_id,
        customer=customer,
    )

    # 2. Store customer message (immutable source of truth)
    customer_msg = await conv_service.add_message(
        conversation,
        sender_type=SenderType.CUSTOMER,
        content=body.message,
    )

    # 3. AI Extraction
    extraction = None
    try:
        extraction = await ai_extractor.extract(
            customer_message=body.message,
            conversation_context="",
            existing_lead=None,
        )
    except AIExtractionError:
        pass  # fallback reply later

    # 4. Persist + qualify
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

    # 5. Trigger n8n (Sheets / notifications later)
    await n8n_service.trigger_chat_processing(
        request_id=request_id,
        conversation_id=conversation.id,
        customer_id=customer.id,
        message_id=customer_msg.id,
        message=body.message,
        lead_id=lead.id if lead else conversation.lead_id,
    )

    # 6. Build reply
    if extraction:
        reply_text = _build_reply(extraction, score=score, temperature=temperature)
        missing = extraction.missing_information
    else:
        reply_text = (
            "Thanks for your message. I've received your enquiry. "
            "Could you tell me your preferred location and budget range?"
        )
        missing = ["location", "budget"]

    # 7. Store bot reply
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
        missing_information=missing,
    )
