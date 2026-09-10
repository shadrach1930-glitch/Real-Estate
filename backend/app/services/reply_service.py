"""
Reply generation service.

Produces natural, progressive responses without inventing inventory or prices.
"""

from app.models.enums import Intent, LeadTemperature
from app.schemas.ai import LeadExtraction


# Priority order for asking missing information (from AI Spec)
MISSING_PRIORITY = [
    "transaction_type",
    "property_type",
    "location",
    "budget",
    "timeline",
    "bedrooms",
    "name",
    "phone",
    "email",
]


def next_missing(missing: list[str]) -> str | None:
    for field in MISSING_PRIORITY:
        if field in missing:
            return field
    return missing[0] if missing else None


def build_reply(
    extraction: LeadExtraction,
    *,
    score: int | None = None,
    temperature: str | None = None,
    customer_name: str | None = None,
) -> str:
    intent = extraction.intent

    # Human escalation
    if intent == Intent.HUMAN_REQUEST:
        return (
            "Absolutely. I'll connect you with a PrimeHomes representative. "
            "Could you please share your name and phone number so they can reach you?"
        )

    # Acknowledge captured requirements
    bits = []
    if extraction.bedrooms:
        bits.append(f"{extraction.bedrooms}-bedroom")
    if extraction.property_type:
        bits.append(extraction.property_type.value.lower().replace("_", " "))
    if extraction.location:
        bits.append(f"in {extraction.location}")
    if extraction.budget_max:
        bits.append(f"with a budget up to ₦{int(extraction.budget_max):,}")
    elif extraction.budget_min:
        bits.append(f"with a budget from ₦{int(extraction.budget_min):,}")

    name_prefix = f"{customer_name}, " if customer_name else ""
    ack = f"{name_prefix}I've noted you're looking for a {' '.join(bits)}. " if bits else name_prefix

    missing = extraction.missing_information or []
    # Don't ask for fields we already have
    if extraction.location and "location" in missing:
        missing = [m for m in missing if m != "location"]
    if (extraction.budget_max or extraction.budget_min) and "budget" in missing:
        missing = [m for m in missing if m != "budget"]
    if extraction.property_type and "property_type" in missing:
        missing = [m for m in missing if m != "property_type"]
    if extraction.timeline and "timeline" in missing:
        missing = [m for m in missing if m != "timeline"]
    if extraction.bedrooms is not None and "bedrooms" in missing:
        missing = [m for m in missing if m != "bedrooms"]
    if extraction.transaction_type and "transaction_type" in missing:
        missing = [m for m in missing if m != "transaction_type"]

    # HOT lead close
    if temperature == LeadTemperature.HOT.value or (score is not None and score >= 80):
        if "phone" in missing or "name" in missing:
            return (
                f"{ack}Your requirements look clear. "
                "A member of our sales team will follow up shortly. "
                "What's the best name and phone number to reach you on?"
            )
        return (
            f"{ack}Thanks — I've captured everything. "
            "A member of our sales team will follow up with you shortly."
        )

    # Progressive single question
    nxt = next_missing(missing)

    questions = {
        "transaction_type": "Are you looking to buy or rent?",
        "property_type": "What type of property are you interested in — apartment, house, duplex, or land?",
        "location": "Which location or area are you interested in?",
        "budget": "What budget range are you working with?",
        "timeline": "When are you looking to move or make a decision?",
        "bedrooms": "How many bedrooms do you need?",
        "name": "What name should I use for your enquiry?",
        "phone": "What's the best phone number for our team to reach you?",
        "email": "Could you share an email address as well?",
    }

    if nxt and nxt in questions:
        return f"{ack}{questions[nxt]}"

    return (
        f"{ack}Thanks, I've captured your requirements. "
        "A member of our sales team will follow up with you shortly."
    )
