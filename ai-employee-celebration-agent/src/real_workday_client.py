from __future__ import annotations

import json
import os
from typing import Any

import requests
from dotenv import load_dotenv

from src.models import Employee


DEFAULT_FIELD_CANDIDATES: dict[str, list[str]] = {
    "employee_id": ["employee_id", "Employee_ID", "Employee ID", "Worker_ID", "Worker ID", "EmployeeID"],
    "worker_id": ["worker_id", "Worker_ID", "Worker ID", "Employee_ID", "Employee ID", "WorkerID"],
    "preferred_name": ["preferred_name", "Preferred_Name", "Preferred Name", "PreferredName", "Name", "Worker"],
    "legal_name": ["legal_name", "Legal_Name", "Legal Name", "LegalName", "Full_Name", "Full Name", "Worker"],
    "email": ["email", "Email", "Email_Address", "Email Address", "Work_Email", "Work Email"],
    "manager_email": ["manager_email", "Manager_Email", "Manager Email", "Manager_Work_Email", "Manager Work Email"],
    "date_of_birth": ["date_of_birth", "Date_of_Birth", "Date of Birth", "Birth_Date", "Birth Date", "DOB"],
    "hire_date": ["hire_date", "Hire_Date", "Hire Date", "Original_Hire_Date", "Original Hire Date"],
    "timezone": ["timezone", "Time_Zone", "Time Zone", "TimeZone", "Default_Time_Zone", "Default Time Zone"],
    "country": ["country", "Country", "Country_Name", "Country Name", "Location_Country", "Location Country"],
    "department": ["department", "Department", "Supervisory_Organization", "Supervisory Organization", "Cost_Center", "Cost Center"],
    "status": ["status", "Status", "Employee_Status", "Employee Status", "Worker_Status", "Worker Status"],
    "celebration_channel": ["celebration_channel", "Celebration_Channel", "Celebration Channel", "Preferred_Channel", "Preferred Channel"],
}


class RealWorkdayRaaSClient:
    """Fetch employee data from a Workday RaaS JSON endpoint.

    The client expects a custom Workday report exposed as RaaS JSON. The report
    should return at least employee ID, worker ID, preferred/legal name, email,
    date of birth, hire date, timezone, country, department, status, and an
    optional celebration channel.
    """

    def __init__(
        self,
        raas_url: str,
        username: str | None = None,
        password: str | None = None,
        access_token: str | None = None,
        verify_ssl: bool = True,
        timeout_seconds: int = 60,
        query_params: dict[str, Any] | None = None,
        field_candidates: dict[str, list[str]] | None = None,
    ) -> None:
        if not raas_url:
            raise ValueError("Workday RaaS URL is required")
        self.raas_url = raas_url
        self.username = username
        self.password = password
        self.access_token = access_token
        self.verify_ssl = verify_ssl
        self.timeout_seconds = timeout_seconds
        self.query_params = query_params or {}
        self.field_candidates = field_candidates or DEFAULT_FIELD_CANDIDATES

    @classmethod
    def from_env(cls) -> "RealWorkdayRaaSClient":
        load_dotenv()
        query_params = _load_json_env("WORKDAY_QUERY_PARAMS_JSON", default={})
        custom_field_map = _load_json_env("WORKDAY_FIELD_MAP_JSON", default={})
        field_candidates = _merge_field_candidates(custom_field_map)

        return cls(
            raas_url=os.getenv("WORKDAY_RAAS_URL") or os.getenv("WORKDAY_RAS_URL") or "",
            username=os.getenv("WORKDAY_USERNAME") or None,
            password=os.getenv("WORKDAY_PASSWORD") or None,
            access_token=os.getenv("WORKDAY_ACCESS_TOKEN") or None,
            verify_ssl=_parse_bool(os.getenv("WORKDAY_VERIFY_SSL", "true")),
            timeout_seconds=int(os.getenv("WORKDAY_TIMEOUT_SECONDS", "60")),
            query_params=query_params,
            field_candidates=field_candidates,
        )

    def fetch_raw(self) -> Any:
        headers = {"Accept": "application/json"}
        auth = None

        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        elif self.username and self.password:
            auth = (self.username, self.password)

        response = requests.get(
            self.raas_url,
            headers=headers,
            auth=auth,
            params=self.query_params,
            timeout=self.timeout_seconds,
            verify=self.verify_ssl,
        )
        response.raise_for_status()
        return response.json()

    def get_all_employees(self) -> list[Employee]:
        return self.rows_to_employees(self.fetch_raw())

    def get_active_employees(self) -> list[Employee]:
        return [employee for employee in self.get_all_employees() if employee.is_active]

    def rows_to_employees(self, payload: Any) -> list[Employee]:
        rows = self.extract_rows(payload)
        employees: list[Employee] = []
        for row in rows:
            employees.append(Employee.from_dict(self._map_row(row)))
        return employees

    def extract_rows(self, payload: Any) -> list[dict[str, Any]]:
        if isinstance(payload, list):
            return [row for row in payload if isinstance(row, dict)]

        if not isinstance(payload, dict):
            raise ValueError("Workday response must be a JSON object or array")

        candidate_keys = [
            "Report_Entry",
            "reportEntry",
            "ReportEntry",
            "data",
            "items",
            "workers",
            "Workers",
            "employees",
            "Employees",
        ]

        for key in candidate_keys:
            value = payload.get(key)
            if isinstance(value, list):
                return [row for row in value if isinstance(row, dict)]
            if isinstance(value, dict):
                nested = value.get("Report_Entry") or value.get("items") or value.get("data")
                if isinstance(nested, list):
                    return [row for row in nested if isinstance(row, dict)]

        raise ValueError(
            "No employee rows found. Expected a Workday RaaS JSON key such as Report_Entry, data, items, or employees."
        )

    def _map_row(self, row: dict[str, Any]) -> dict[str, Any]:
        return {
            "employee_id": self._pick(row, "employee_id"),
            "worker_id": self._pick(row, "worker_id"),
            "preferred_name": self._pick(row, "preferred_name") or self._pick(row, "legal_name"),
            "legal_name": self._pick(row, "legal_name") or self._pick(row, "preferred_name"),
            "email": self._pick(row, "email"),
            "manager_email": self._pick(row, "manager_email"),
            "date_of_birth": self._pick(row, "date_of_birth"),
            "hire_date": self._pick(row, "hire_date"),
            "timezone": self._pick(row, "timezone") or os.getenv("DEFAULT_EMPLOYEE_TIMEZONE", "UTC"),
            "country": self._pick(row, "country"),
            "department": self._pick(row, "department"),
            "status": self._pick(row, "status") or "Active",
            "celebration_channel": self._pick(row, "celebration_channel") or "Email",
        }

    def _pick(self, row: dict[str, Any], normalized_field: str) -> Any:
        candidates = self.field_candidates.get(normalized_field, [])
        for key in candidates:
            if key in row:
                return _unwrap_workday_value(row[key])

        lower_key_map = {str(key).lower().replace(" ", "_"): key for key in row.keys()}
        for key in candidates:
            normalized_key = key.lower().replace(" ", "_")
            actual_key = lower_key_map.get(normalized_key)
            if actual_key is not None:
                return _unwrap_workday_value(row[actual_key])

        return None


def _unwrap_workday_value(value: Any) -> Any:
    if isinstance(value, dict):
        for key in ("value", "Value", "descriptor", "Descriptor", "$value", "displayValue", "id", "ID"):
            if key in value and value[key] not in (None, ""):
                return _unwrap_workday_value(value[key])
        return json.dumps(value, ensure_ascii=False)

    if isinstance(value, list):
        if not value:
            return None
        unwrapped = [_unwrap_workday_value(item) for item in value]
        unwrapped = [item for item in unwrapped if item not in (None, "")]
        return ", ".join(str(item) for item in unwrapped) if unwrapped else None

    return value


def _parse_bool(value: str | None) -> bool:
    return str(value or "").strip().lower() not in {"false", "0", "no", "n"}


def _load_json_env(name: str, default: Any) -> Any:
    raw = os.getenv(name)
    if not raw:
        return default
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Environment variable {name} must contain valid JSON") from exc


def _merge_field_candidates(custom_field_map: dict[str, Any]) -> dict[str, list[str]]:
    merged = {key: list(values) for key, values in DEFAULT_FIELD_CANDIDATES.items()}
    for normalized_field, custom_value in custom_field_map.items():
        if isinstance(custom_value, str):
            merged[normalized_field] = [custom_value] + merged.get(normalized_field, [])
        elif isinstance(custom_value, list):
            merged[normalized_field] = [str(item) for item in custom_value] + merged.get(normalized_field, [])
    return merged
