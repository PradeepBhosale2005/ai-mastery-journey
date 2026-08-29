from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date, datetime
from typing import Any, Optional


def parse_date(value: Any) -> Optional[date]:
    """Parse an ISO date string into a date object."""
    if value in (None, ""):
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    return datetime.strptime(str(value), "%Y-%m-%d").date()


@dataclass(frozen=True)
class Employee:
    employee_id: str
    worker_id: str
    preferred_name: str
    legal_name: str
    email: str
    manager_email: str
    date_of_birth: Optional[date]
    hire_date: Optional[date]
    timezone: str
    country: str
    department: str
    status: str
    celebration_channel: str

    @classmethod
    def from_dict(cls, row: dict[str, Any]) -> "Employee":
        return cls(
            employee_id=str(row.get("employee_id", "")),
            worker_id=str(row.get("worker_id", "")),
            preferred_name=str(row.get("preferred_name", row.get("legal_name", ""))),
            legal_name=str(row.get("legal_name", "")),
            email=str(row.get("email", "")),
            manager_email=str(row.get("manager_email", "")),
            date_of_birth=parse_date(row.get("date_of_birth")),
            hire_date=parse_date(row.get("hire_date")),
            timezone=str(row.get("timezone", "UTC")),
            country=str(row.get("country", "")),
            department=str(row.get("department", "")),
            status=str(row.get("status", "Inactive")),
            celebration_channel=str(row.get("celebration_channel", "Email")),
        )

    @property
    def is_active(self) -> bool:
        return self.status.strip().lower() == "active"

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["date_of_birth"] = self.date_of_birth.isoformat() if self.date_of_birth else None
        data["hire_date"] = self.hire_date.isoformat() if self.hire_date else None
        return data


@dataclass(frozen=True)
class CelebrationEvent:
    employee: Employee
    event_type: str
    celebration_date: date
    years: Optional[int]
    local_date: date
    source_system: str = "Mock Workday API"

    def to_dict(self) -> dict[str, Any]:
        return {
            "employee_id": self.employee.employee_id,
            "worker_id": self.employee.worker_id,
            "preferred_name": self.employee.preferred_name,
            "email": self.employee.email,
            "manager_email": self.employee.manager_email,
            "department": self.employee.department,
            "country": self.employee.country,
            "timezone": self.employee.timezone,
            "event_type": self.event_type,
            "celebration_date": self.celebration_date.isoformat(),
            "years": self.years,
            "local_date": self.local_date.isoformat(),
            "channel": self.employee.celebration_channel,
            "source_system": self.source_system,
        }


@dataclass(frozen=True)
class NotificationResult:
    employee_id: str
    event_type: str
    channel: str
    recipient: str
    message: str
    status: str
    simulated: bool
    timestamp_utc: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
