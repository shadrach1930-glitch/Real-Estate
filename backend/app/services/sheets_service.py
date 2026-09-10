"""
Google Sheets sync service.

When credentials + spreadsheet ID are configured, new/updated leads
are appended (or updated) in a sheet for operational visibility.

Graceful no-op when not configured.
"""

import logging
from typing import Any

from app.config import settings

logger = logging.getLogger(__name__)


class SheetsService:
    def __init__(self):
        self.spreadsheet_id = settings.google_sheets_id
        self.credentials_path = settings.google_sheets_credentials
        self._client = None

    @property
    def is_configured(self) -> bool:
        return bool(self.spreadsheet_id and self.credentials_path)

    def _get_client(self):
        if self._client is not None:
            return self._client

        if not self.is_configured:
            return None

        try:
            import gspread
            from google.oauth2.service_account import Credentials

            scopes = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive",
            ]
            creds = Credentials.from_service_account_file(
                self.credentials_path, scopes=scopes
            )
            self._client = gspread.authorize(creds)
            return self._client
        except Exception as exc:
            logger.warning("Google Sheets client init failed: %s", exc)
            return None

    async def sync_lead(self, lead_data: dict[str, Any]) -> bool:
        """
        Append or update a lead row in the configured spreadsheet.

        Expected keys in lead_data:
          id, customer_name, phone, email, property_type, location,
          budget, score, temperature, status, created_at
        """
        if not self.is_configured:
            logger.debug("Sheets not configured — skipping sync")
            return False

        try:
            client = self._get_client()
            if not client:
                return False

            sheet = client.open_by_key(self.spreadsheet_id).sheet1

            # Ensure header row exists
            headers = [
                "Lead ID",
                "Customer",
                "Phone",
                "Email",
                "Property Type",
                "Location",
                "Budget",
                "Score",
                "Temperature",
                "Status",
                "Created At",
            ]
            existing = sheet.row_values(1)
            if not existing:
                sheet.append_row(headers)

            row = [
                str(lead_data.get("id", "")),
                lead_data.get("customer_name") or "",
                lead_data.get("phone") or "",
                lead_data.get("email") or "",
                lead_data.get("property_type") or "",
                lead_data.get("location") or "",
                str(lead_data.get("budget") or ""),
                str(lead_data.get("score") or ""),
                lead_data.get("temperature") or "",
                lead_data.get("status") or "",
                str(lead_data.get("created_at") or ""),
            ]

            # Try to find existing row by Lead ID (column A)
            try:
                cell = sheet.find(str(lead_data.get("id", "")), in_column=1)
                if cell:
                    sheet.update(f"A{cell.row}:K{cell.row}", [row])
                    logger.info("Updated lead %s in Google Sheets", lead_data.get("id"))
                    return True
            except Exception:
                pass  # not found → append

            sheet.append_row(row)
            logger.info("Appended lead %s to Google Sheets", lead_data.get("id"))
            return True

        except Exception as exc:
            logger.error("Google Sheets sync failed: %s", exc)
            return False


sheets_service = SheetsService()
