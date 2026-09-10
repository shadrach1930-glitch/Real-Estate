"""Dashboard schemas."""

from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_leads: int = 0
    new_leads: int = 0
    hot_leads: int = 0
    warm_leads: int = 0
    cold_leads: int = 0
    qualified_leads: int = 0
    converted_leads: int = 0
    pending_follow_ups: int = 0
