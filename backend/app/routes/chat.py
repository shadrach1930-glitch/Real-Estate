"""
POST /api/v1/chat

Flow (Phase 6):
  1. Validate + store customer message
  2. Run AI extraction (or fallback)
  3. Trigger n8n (optional orchestration)
  4. Generate / return reply
"""

from uuid import uuid4

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db
from app.models.enums import Intent, SenderType
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.ai import ai_extractor, AIExtractionError
from app.services.conversation_service import ConversationService
from app.services.n8n_service import n8n_service

router = APIRouter()


def _build_reply(extraction) -> str:
    """Simple rule-based reply generator (full AI response gen comes later)."""
    intent = extraction.intent

    if intent == Intent.HUMAN_REQUEST:
        return (
            "Absolutely. I'll connect you with a PrimeHomes representative. "
            "Could you please share your name and phone number so they can reach you?"
        )

    parts = []
    if extraction.property_type or extraction.location or extraction.bedrooms:
        bits = []
        if extraction.bedrooms:
            bits.append(f"{extraction.bedrooms}-bedroom")
        if extraction.property_type:
            bits.append(extraction.property_type.value.lower())
        if extraction.location:
            bits.append(f"in {extraction.location}")
        parts.append(f"I've noted you're looking for a {' '.join(bits)}." if bits else "")

    missing = extraction.missing_information or []
    # Priority questions
    if "location" in missing:
        parts.append("Which location are you interested in?")
    elif "budget" in missing:
        parts.append("What budget range are you working with?")
    elif "property_type" in missing:
        parts.append("What type of property are you looking for (apartment, house, duplex, land)?")
    elif "timeline" in missing:
        parts.append("When are you looking to buy or rent?")
    elif "name" in missing or "phone" in missing:
        parts.append("Could you share your name and a phone number so our team can follow up?")
    else:
        parts.append(
            "Thanks, I've captured your requirements. "
            "A member of our sales team will follow up with you shortly."
        )

    return " ".join(p for p in parts if p).strip()


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

    # 2. Store customer message
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
    except AIExtractionError as exc:
        # Log and continue with safe fallback
        import logging
        logging.getLogger(__name__).warning(
            "AI extraction failed (%s): %s", exc.code, exc.message
        )

    # 4. Trigger n8n (still useful for Sheets / notifications later)
    n8n_result = await n8n_service.trigger_chat_processing(
        request_id=request_id,
        conversation_id=conversation.id,
        customer_id=customer.id,
        message_id=customer_msg.id,
        message=body.message,
        lead_id=conversation.lead_id,
    )

    # 5. Build reply
    if n8n_result and n8n_result.get("reply"):
        reply_text = n8n_result["reply"]
        missing = n8n_result.get("missing_information", [])
    elif extraction:
        reply_text = _build_reply(extraction)
        missing = extraction.missing_information
    else:
        reply_text = (
            "Thanks for your message. I've received your enquiry. "
            "Could you tell me your preferred location and budget range?"
        )
        missing = ["location", "budget"]

    # 6. Store bot reply
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
        missing_information=missing,
    )
