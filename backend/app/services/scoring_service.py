"""
Deterministic lead scoring service.

Scoring rules (from Database Design & PRD):

  Phone provided          +10
  Budget provided         +20
  Location provided       +15
  Property type provided  +15
  Buying/renting soon     +25
  Clear requirements       +15

  Max = 100

  80–100 → HOT
  50–79  → WARM
   0–49  → COLD
"""

from app.models.enums import LeadTemperature, Timeline
from app.models.lead import Lead, PropertyRequirement
from app.models.customer import Customer


def calculate_score(
    *,
    has_phone: bool = False,
    has_budget: bool = False,
    has_location: bool = False,
    has_property_type: bool = False,
    timeline: Timeline | None = None,
    has_clear_requirements: bool = False,
) -> tuple[int, LeadTemperature, str]:
    score = 0
    reasons: list[str] = []

    if has_phone:
        score += 10
        reasons.append("phone provided (+10)")

    if has_budget:
        score += 20
        reasons.append("budget provided (+20)")

    if has_location:
        score += 15
        reasons.append("location provided (+15)")

    if has_property_type:
        score += 15
        reasons.append("property type provided (+15)")

    if timeline in (Timeline.IMMEDIATE, Timeline.WITHIN_1_MONTH):
        score += 25
        reasons.append("urgent timeline (+25)")
    elif timeline == Timeline.WITHIN_3_MONTHS:
        score += 15
        reasons.append("near-term timeline (+15)")

    if has_clear_requirements:
        score += 15
        reasons.append("clear requirements (+15)")

    score = min(score, 100)

    if score >= 80:
        temperature = LeadTemperature.HOT
    elif score >= 50:
        temperature = LeadTemperature.WARM
    else:
        temperature = LeadTemperature.COLD

    reason = "; ".join(reasons) if reasons else "Insufficient information"
    return score, temperature, reason


def score_lead(lead: Lead, customer: Customer | None = None) -> tuple[int, LeadTemperature, str]:
    """Score a Lead instance using its related data."""
    req: PropertyRequirement | None = lead.property_requirement

    has_phone = bool(customer and customer.phone) if customer else False
    has_budget = bool(req and (req.budget_min is not None or req.budget_max is not None))
    has_location = bool(req and req.location)
    has_property_type = bool(req and req.property_type)
    timeline = req.timeline if req else None

    # Clear requirements = at least property_type + location + (budget or bedrooms)
    has_clear = bool(
        has_property_type
        and has_location
        and (has_budget or (req and req.bedrooms is not None))
    )

    return calculate_score(
        has_phone=has_phone,
        has_budget=has_budget,
        has_location=has_location,
        has_property_type=has_property_type,
        timeline=timeline,
        has_clear_requirements=has_clear,
    )
