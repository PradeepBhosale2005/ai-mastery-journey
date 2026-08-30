from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any

import requests
from dotenv import load_dotenv


@dataclass(frozen=True)
class ActualReportEmployee:
    employee_id: str
    preferred_name: str
    legal_first_name: str
    legal_last_name: str
    email: str
    manager_email: str
    status: str
    country: str
    next_birthday_date: date | None
    original_hire_date: date | None
    supervisory_organization: str
    timezone_raw: str
    timezone: str
    celebration_channel: str = "Email"

    @property
    def is_active(self) -> bool:
        return self.status.strip().lower() in {"active", "yes", "true", "1"}

    @property
    def legal_name(self) -> str:
        return " ".join(part for part in [self.legal_first_name, self.legal_last_name] if part).strip()

    @property
    def display_name(self) -> str:
        return self.preferred_name or self.legal_name or self.employee_id

    def to_event_employee_dict(self) -> dict[str, Any]:
        return {
            "employee_id": self.employee_id,
            "worker_id": self.employee_id,
            "preferred_name": self.display_name,
            "legal_name": self.legal_name or self.display_name,
            "email": self.email,
            "manager_email": self.manager_email,
            "date_of_birth": None,
            "hire_date": self.original_hire_date.isoformat() if self.original_hire_date else None,
            "timezone": self.timezone,
            "country": self.country,
            "department": self.supervisory_organization,
            "status": self.status,
            "celebration_channel": self.celebration_channel,
        }

    def preview_dict(self) -> dict[str, Any]:
        return {
            "employee_id": self.employee_id,
            "preferred_name": self.display_name,
            "email_present": bool(self.email),
            "manager_email_present": bool(self.manager_email),
            "status": self.status,
            "country": self.country,
            "next_birthday_date": self.next_birthday_date.isoformat() if self.next_birthday_date else None,
            "original_hire_date_present": bool(self.original_hire_date),
            "supervisory_organization": self.supervisory_organization,
            "timezone_raw": self.timezone_raw,
            "timezone_normalized": self.timezone,
        }


class ActualWorkdayReportClient:
    """Client for the exact RPT_AI_Employee_Celebration_Agent RaaS JSON report."""

    def __init__(
        self,
        report_url: str,
        username: str | None = None,
        password: str | None = None,
        access_token: str | None = None,
        verify_ssl: bool = True,
        timeout_seconds: int = 60,
    ) -> None:
        if not report_url:
            raise ValueError("WORKDAY_RAAS_URL is required")
        self.report_url = report_url
        self.username = username
        self.password = password
        self.access_token = access_token
        self.verify_ssl = verify_ssl
        self.timeout_seconds = timeout_seconds

    @classmethod
    def from_env(cls) -> "ActualWorkdayReportClient":
        load_dotenv()
        return cls(
            report_url=os.getenv("WORKDAY_RAAS_URL") or os.getenv("WORKDAY_RAS_URL") or "",
            username=os.getenv("WORKDAY_USERNAME") or None,
            password=os.getenv("WORKDAY_PASSWORD") or None,
            access_token=os.getenv("WORKDAY_ACCESS_TOKEN") or None,
            verify_ssl=_parse_bool(os.getenv("WORKDAY_VERIFY_SSL", "true")),
            timeout_seconds=int(os.getenv("WORKDAY_TIMEOUT_SECONDS", "60")),
        )

    def fetch_raw(self) -> Any:
        headers = {"Accept": "application/json"}
        auth = None

        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        elif self.username and self.password:
            auth = (self.username, self.password)

        response = requests.get(
            self.report_url,
            headers=headers,
            auth=auth,
            timeout=self.timeout_seconds,
            verify=self.verify_ssl,
        )
        response.raise_for_status()
        return response.json()

    def get_all_employees(self) -> list[ActualReportEmployee]:
        return self.rows_to_employees(self.fetch_raw())

    def get_active_employees(self) -> list[ActualReportEmployee]:
        return [employee for employee in self.get_all_employees() if employee.is_active]

    def rows_to_employees(self, payload: Any) -> list[ActualReportEmployee]:
        rows = _extract_report_entries(payload)
        return [_row_to_employee(row) for row in rows]


def _extract_report_entries(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]

    if not isinstance(payload, dict):
        raise ValueError("Report response must be a JSON object or array")

    entries = payload.get("Report_Entry")
    if isinstance(entries, list):
        return [row for row in entries if isinstance(row, dict)]

    raise ValueError("Expected Workday RaaS JSON with a Report_Entry array")


def _row_to_employee(row: dict[str, Any]) -> ActualReportEmployee:
    timezone_raw = str(_get(row, "Time_Zone_of_Location_of_Worker_s_Primary_Position") or "")
    return ActualReportEmployee(
        employee_id=str(_get(row, "Employee_ID") or ""),
        preferred_name=str(_get(row, "Preferred_Name") or ""),
        legal_first_name=str(_get(row, "Legal_Name_-_First_Name") or ""),
        legal_last_name=str(_get(row, "Legal_Name_-_Last_Name") or ""),
        email=str(_get(row, "Email_-_Primary_Work_or_Primary_Home") or ""),
        manager_email=str(_get(row, "CF-LRV-Manager_Email_Id") or ""),
        status=str(_get(row, "Active") or "Inactive"),
        country=str(_get(row, "Country_of_position_location_on_worker_profile") or ""),
        next_birthday_date=_parse_date(_get(row, "Date_of_Workers_Next_Birthday")),
        original_hire_date=_parse_date(_get(row, "Original_Hire_Date")),
        supervisory_organization=str(_get(row, "Supervisory_Organization") or ""),
        timezone_raw=timezone_raw,
        timezone=_normalize_workday_timezone(timezone_raw),
        celebration_channel="Email",
    )


def _get(row: dict[str, Any], key: str) -> Any:
    value = row.get(key)
    if isinstance(value, dict):
        for nested_key in ("value", "Value", "descriptor", "Descriptor", "$value", "displayValue"):
            if nested_key in value:
                return value[nested_key]
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, list):
        values = [_get({"value": item}, "value") for item in value]
        values = [item for item in values if item not in (None, "")]
        return ", ".join(str(item) for item in values)
    return value


def _parse_date(value: Any) -> date | None:
    if value in (None, ""):
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    return datetime.strptime(str(value)[:10], "%Y-%m-%d").date()


def _parse_bool(value: str | None) -> bool:
    return str(value or "").strip().lower() not in {"false", "0", "no", "n"}


def _normalize_workday_timezone(value: str) -> str:
    text = value.strip().lower()
    if not text:
        return os.getenv("DEFAULT_EMPLOYEE_TIMEZONE", "UTC")

    mappings = [
        ("los angeles", "America/Los_Angeles"),
        ("pacific", "America/Los_Angeles"),
        ("new york", "America/New_York"),
        ("eastern", "America/New_York"),
        ("chicago", "America/Chicago"),
        ("central", "America/Chicago"),
        ("denver", "America/Denver"),
        ("mountain", "America/Denver"),
        ("kolkata", "Asia/Kolkata"),
        ("india", "Asia/Kolkata"),
        ("london", "Europe/London"),
        ("utc", "UTC"),
        ("gmt", "UTC"),
    ]
    for marker, zone in mappings:
        if marker in text:
            return zone

    # Already an IANA zone such as America/Los_Angeles.
    if re.match(r"^[A-Za-z_]+/[A-Za-z_]+", value.strip()):
        return value.strip()

    return os.getenv("DEFAULT_EMPLOYEE_TIMEZONE", "UTC")
