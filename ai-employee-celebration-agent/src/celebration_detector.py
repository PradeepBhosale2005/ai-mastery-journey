from __future__ import annotations

from datetime import date, datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from src.models import CelebrationEvent, Employee


def _safe_zoneinfo(timezone_name: str) -> ZoneInfo:
    try:
        return ZoneInfo(timezone_name)
    except ZoneInfoNotFoundError:
        return ZoneInfo("UTC")


def employee_local_date(run_at: date | datetime, timezone_name: str) -> date:
    """Return the employee-local business date for a run date or timestamp."""
    if isinstance(run_at, datetime):
        aware_run_at = run_at if run_at.tzinfo else run_at.replace(tzinfo=timezone.utc)
        return aware_run_at.astimezone(_safe_zoneinfo(timezone_name)).date()
    return run_at


def _same_month_day(value: date | None, target_date: date) -> bool:
    if value is None:
        return False
    return value.month == target_date.month and value.day == target_date.day


def _years_since(start_date: date, target_date: date) -> int:
    years = target_date.year - start_date.year
    if (target_date.month, target_date.day) < (start_date.month, start_date.day):
        years -= 1
    return years


class CelebrationDetector:
    """Detect active employee birthdays and work anniversaries."""

    def find_events(self, employees: list[Employee], run_at: date | datetime) -> list[CelebrationEvent]:
        events: list[CelebrationEvent] = []

        for employee in employees:
            if not employee.is_active:
                continue

            local_run_date = employee_local_date(run_at, employee.timezone)

            if _same_month_day(employee.date_of_birth, local_run_date):
                events.append(
                    CelebrationEvent(
                        employee=employee,
                        event_type="birthday",
                        celebration_date=employee.date_of_birth,
                        years=None,
                        local_date=local_run_date,
                    )
                )

            if employee.hire_date and _same_month_day(employee.hire_date, local_run_date):
                anniversary_years = _years_since(employee.hire_date, local_run_date)
                if anniversary_years > 0:
                    events.append(
                        CelebrationEvent(
                            employee=employee,
                            event_type="work_anniversary",
                            celebration_date=employee.hire_date,
                            years=anniversary_years,
                            local_date=local_run_date,
                        )
                    )

        return events
