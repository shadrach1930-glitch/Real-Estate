"""
AI Lead Extraction service.

Principle: "AI interprets. The backend validates. The database stores."
"""

import json
import logging
import re
from typing import Any

import httpx

from app.config import settings
from app.schemas.ai import LeadExtraction
from app.services.ai.prompts import (
    EXTRACTION_PROMPT_V1,
    PROMPT_VERSIONS,
    SYSTEM_PROMPT_V1,
)
from app.services.ai.normalization import (
    normalize_budget,
    normalize_bedrooms,
    normalize_property_type,
    normalize_timeline,
)

logger = logging.getLogger(__name__)


class AIExtractionError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(message)


class AIExtractor:
    """Configurable LLM-based lead information extractor."""

    def __init__(self):
        self.provider = settings.ai_provider
        self.model = settings.ai_model
        self.api_key = settings.ai_api_key
        self.temperature = settings.ai_temperature
        self.max_tokens = settings.ai_max_tokens

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key and self.model)

    async def extract(
        self,
        *,
        customer_message: str,
        conversation_context: str = "",
        existing_lead: dict[str, Any] | None = None,
    ) -> LeadExtraction:
        """
        Run AI-001 Lead Information Extraction.

        Returns a validated LeadExtraction object.
        Raises AIExtractionError on failure.
        """
        if not self.is_configured:
            # Deterministic fallback when no AI key is configured (dev mode)
            return self._fallback_extract(customer_message)

        prompt = EXTRACTION_PROMPT_V1.format(
            existing_lead=json.dumps(existing_lead or {}, default=str),
            conversation_context=conversation_context or "(none)",
            customer_message=customer_message,
        )

        raw = await self._call_model(system=SYSTEM_PROMPT_V1, user=prompt)
        data = self._parse_json(raw)
        data = self._post_normalize(data)

        try:
            extraction = LeadExtraction.model_validate(data)
        except Exception as exc:
            raise AIExtractionError("AI_SCHEMA_ERROR", f"Schema validation failed: {exc}") from exc

        return extraction

    async def _call_model(self, *, system: str, user: str) -> str:
        """Call the configured LLM provider. Currently supports OpenAI-compatible APIs."""
        # Generic OpenAI-compatible endpoint (works with many providers)
        url = "https://api.openai.com/v1/chat/completions"
        if self.provider == "google":
            # Placeholder — swap for actual Google/Gemini endpoint when key is set
            url = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "response_format": {"type": "json_object"},
        }

        try:
            async with httpx.AsyncClient(timeout=45.0) as client:
                resp = await client.post(url, headers=headers, json=payload)

                if resp.status_code == 429:
                    raise AIExtractionError("AI_RATE_LIMIT", "Rate limit exceeded")
                if resp.status_code >= 500:
                    raise AIExtractionError("AI_PROVIDER_ERROR", f"Provider error {resp.status_code}")
                if resp.status_code >= 400:
                    raise AIExtractionError("AI_PROVIDER_ERROR", resp.text[:300])

                body = resp.json()
                content = body["choices"][0]["message"]["content"]
                return content

        except httpx.TimeoutException as exc:
            raise AIExtractionError("AI_TIMEOUT", "AI request timed out") from exc
        except AIExtractionError:
            raise
        except Exception as exc:
            raise AIExtractionError("AI_PROVIDER_ERROR", str(exc)) from exc

    def _parse_json(self, raw: str) -> dict:
        """Extract JSON from model output (handles markdown fences)."""
        text = raw.strip()

        # Strip ```json ... ``` if present
        fence = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
        if fence:
            text = fence.group(1).strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise AIExtractionError("AI_INVALID_JSON", f"Invalid JSON: {exc}") from exc

    def _post_normalize(self, data: dict) -> dict:
        """Apply deterministic normalization after AI extraction."""
        if "budget_max" in data and data["budget_max"] is not None:
            data["budget_max"] = normalize_budget(data["budget_max"])
        if "budget_min" in data and data["budget_min"] is not None:
            data["budget_min"] = normalize_budget(data["budget_min"])

        if data.get("property_type") and isinstance(data["property_type"], str):
            normalized = normalize_property_type(data["property_type"])
            if normalized:
                data["property_type"] = normalized

        if data.get("bedrooms") is not None:
            data["bedrooms"] = normalize_bedrooms(data["bedrooms"])

        if data.get("timeline") and isinstance(data["timeline"], str):
            normalized = normalize_timeline(data["timeline"])
            if normalized:
                data["timeline"] = normalized

        return data

    def _fallback_extract(self, message: str) -> LeadExtraction:
        """
        Lightweight rule-based extraction used when no AI key is configured.
        Useful for local development and testing the pipeline.
        """
        msg = message.lower()
        data: dict[str, Any] = {
            "intent": "OTHER",
            "currency": "NGN",
            "customer": {},
            "additional_requirements": [],
            "missing_information": [],
            "confidence": {"overall": 0.5},
        }

        if any(w in msg for w in ("buy", "purchase", "own")):
            data["intent"] = "BUY"
            data["transaction_type"] = "BUY"
        elif any(w in msg for w in ("rent", "rental", "lease")):
            data["intent"] = "RENT"
            data["transaction_type"] = "RENT"
        elif "land" in msg or "plot" in msg:
            data["intent"] = "LAND"
            data["property_type"] = "LAND"
        elif any(w in msg for w in ("agent", "human", "speak to", "talk to", "representative")):
            data["intent"] = "HUMAN_REQUEST"

        pt = normalize_property_type(msg)
        if pt:
            data["property_type"] = pt

        beds = normalize_bedrooms(msg)
        if beds:
            data["bedrooms"] = beds

        # Simple location heuristics (common Lagos areas)
        for loc in ("lekki", "ikoyi", "victoria island", "vi", "ajah", "ikeja", "yaba",
                    "surulere", "maryland", "gbagada", "magodo", "banana island",
                    "abuja", "maitama", "wuse", "ibadan"):
            if loc in msg:
                data["location"] = loc.title()
                break

        # Budget
        budget_match = re.search(r"(?:₦|naira|ngn|budget)?\s*([\d,.]+)\s*(m|million|k)?", msg)
        if budget_match:
            raw_budget = budget_match.group(0)
            val = normalize_budget(raw_budget)
            if val:
                data["budget_max"] = val

        tl = normalize_timeline(msg)
        if tl:
            data["timeline"] = tl

        # Missing information priority
        missing = []
        if not data.get("transaction_type") and data["intent"] not in ("LAND", "HUMAN_REQUEST"):
            missing.append("transaction_type")
        if not data.get("property_type"):
            missing.append("property_type")
        if not data.get("location"):
            missing.append("location")
        if not data.get("budget_max") and not data.get("budget_min"):
            missing.append("budget")
        if not data.get("timeline"):
            missing.append("timeline")

        data["missing_information"] = missing
        data["confidence"]["overall"] = 0.6 if (data.get("location") or data.get("budget_max")) else 0.4

        return LeadExtraction.model_validate(data)


# Singleton
ai_extractor = AIExtractor()
