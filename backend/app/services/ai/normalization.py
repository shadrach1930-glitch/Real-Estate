"""
Normalization helpers for Nigerian real-estate terminology and currency.
"""

import re
from decimal import Decimal, InvalidOperation
from typing import Any


def normalize_budget(value: Any) -> Decimal | None:
    """
    Convert common Nigerian budget expressions to a numeric value.

    Examples:
      "80m" / "80 million" / "₦80m" / "N80M" / "80,000,000" → 80000000
    """
    if value is None:
        return None

    if isinstance(value, (int, float, Decimal)):
        return Decimal(str(value))

    text = str(value).strip().lower()
    text = text.replace(",", "").replace("₦", "").replace("naira", "").replace("ngn", "")
    text = text.strip()

    # Pattern: number + optional multiplier
    match = re.match(r"^([\d.]+)\s*(m|million|k|thousand)?$", text)
    if not match:
        try:
            return Decimal(text)
        except (InvalidOperation, ValueError):
            return None

    number = Decimal(match.group(1))
    multiplier = match.group(2)

    if multiplier in ("m", "million"):
        number *= Decimal("1000000")
    elif multiplier in ("k", "thousand"):
        number *= Decimal("1000")

    return number


def normalize_property_type(text: str | None) -> str | None:
    if not text:
        return None

    t = text.lower().strip()

    mapping = {
        "apartment": "APARTMENT",
        "flat": "APARTMENT",
        "appart": "APARTMENT",
        "house": "HOUSE",
        "bungalow": "HOUSE",
        "duplex": "DUPLEX",
        "semi-detached": "DUPLEX",
        "detached": "HOUSE",
        "villa": "VILLA",
        "land": "LAND",
        "plot": "LAND",
        "plot of land": "LAND",
        "office": "OFFICE",
        "shop": "SHOP",
        "commercial": "COMMERCIAL",
    }

    for key, value in mapping.items():
        if key in t:
            return value

    return None


def normalize_bedrooms(text: str | None) -> int | None:
    if text is None:
        return None
    if isinstance(text, int):
        return text

    t = str(text).lower()
    match = re.search(r"(\d+)\s*(?:bed|bedroom|br|bhk)?", t)
    if match:
        return int(match.group(1))

    word_map = {
        "one": 1, "two": 2, "three": 3, "four": 4,
        "five": 5, "six": 6, "seven": 7,
    }
    for word, num in word_map.items():
        if word in t:
            return num

    return None


def normalize_timeline(text: str | None) -> str | None:
    if not text:
        return None

    t = text.lower()

    if any(w in t for w in ("immediate", "asap", "right away", "now", "this week")):
        return "IMMEDIATE"
    if any(w in t for w in ("this month", "1 month", "one month", "within a month")):
        return "WITHIN_1_MONTH"
    if any(w in t for w in ("2 month", "3 month", "two month", "three month", "within 3")):
        return "WITHIN_3_MONTHS"
    if any(w in t for w in ("6 month", "six month", "within 6")):
        return "WITHIN_6_MONTHS"
    if any(w in t for w in ("research", "just looking", "checking", "browsing")):
        return "RESEARCHING"

    return None
