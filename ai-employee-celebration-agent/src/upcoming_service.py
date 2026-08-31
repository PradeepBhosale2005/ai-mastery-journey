from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Any

from src.actual_report_client import ActualReportEmployee
from src.models import CelebrationEvent, Employee


@dataclass(frozen=True)
class PlannedCelebration:
    """A celebration event planned for today or an upcoming date."""

    event: CelebrationEvent
    event_date: date
    days_until: int

    @property
    def is_today(self) -> bool:
        return self.days_until == 0

    @property
    def priority_label(self) -> str:
        if self.days_until == 0:
            return "Due Today"
        if self.days_until == 1:
            return "Tomorrow"
        return f"In {self.days_until} days"

    def to_dict(self) -> dict[str, Any]:
        data = self.event.to_dict()
        data["event_date"] = self.event_date.isoformat()
        data["days_until"] = self.days_until
        data["priority_label"] = self.priority_label
        data["is_today"] = self.is_today
        return data


def find_planned_celebrations(
    employees: list[ActualReportEmployee],
    run_date: date | datetime,
    lookahead_days: int = 30,
    include_today: bool = True,
) -> list[PlannedCelebration]:
    """Find due and upcoming birthdays/work anniversaries from the Workday report.

    Birthday detection uses the Workday calculated field Date_of_Workers_Next_Birthday.
    Work anniversary detection calculates the next occurrence from Original_Hire_Date.
    """
    business_date = _as_date(run_date)
    window_start = business_date if include_today else business_date + timedelta(days=1)
    window_end = business_date + timedelta(days=max(0, lookahead_days))
    planned: list[PlannedCelebration] = []

    for report_employee in employees:
        if not report_employee.is_active:
            continue

        event_employee = Employee.from_dict(report_employee.to_event_employee_dict())

        birthday_date = report_employee.next_birthday_date
        if birthday_date and window_start <= birthday_date <= window_end:
            planned.append(
                PlannedCelebration(
                    event=CelebrationEvent(
                        employee=event_employee,
                        event_type="birthday",
                        celebration_date=birthday_date,
                        years=None,
                        local_date=birthday_date,
                        source_system="Workday RaaS Report",
                    ),
                    event_date=birthday_date,
                    days_until=(birthday_date - business_date).days,
                )
            )

        if report_employee.original_hire_date:
            anniversary_date = _next_occurrence(report_employee.original_hire_date, business_date)
            years = anniversary_date.year - report_employee.original_hire_date.year
            if years > 0 and window_start <= anniversary_date <= window_end:
                planned.append(
                    PlannedCelebration(
                        event=CelebrationEvent(
                            employee=event_employee,
                            event_type="work_anniversary",
                            celebration_date=report_employee.original_hire_date,
                            years=years,
                            local_date=anniversary_date,
                            source_system="Workday RaaS Report",
                        ),
                        event_date=anniversary_date,
                        days_until=(anniversary_date - business_date).days,
                    )
                )

    return sorted(
        planned,
        key=lambda item: (
            item.event_date,
            item.event.event_type,
            item.event.employee.preferred_name.lower(),
        ),
    )


def planned_to_table(planned: list[PlannedCelebration]) -> list[dict[str, Any]]:
    """Return UI-friendly table rows."""
    rows: list[dict[str, Any]] = []
    for item in planned:
        event = item.event
        employee = event.employee
        rows.append(
            {
                "Priority": item.priority_label,
                "Event Date": item.event_date.isoformat(),
                "Days Until": item.days_until,
                "Event Type": _label_event_type(event.event_type),
                "Employee ID": employee.employee_id,
                "Name": employee.preferred_name,
                "Email": employee.email,
                "Manager Email": employee.manager_email,
                "Department": employee.department,
                "Country": employee.country,
                "Years": event.years or "",
                "Channel": employee.celebration_channel,
            }
        )
    return rows


def _label_event_type(event_type: str) -> str:
    return "Birthday" if event_type == "birthday" else "Work Anniversary"


def _as_date(value: date | datetime) -> date:
    if isinstance(value, datetime):
        return value.date()
    return value


def _next_occurrence(start_date: date, from_date: date) -> date:
    candidate = _safe_date(from_date.year, start_date.month, start_date.day)
    if candidate < from_date:
        candidate = _safe_date(from_date.year + 1, start_date.month, start_date.day)
    return candidate


def _safe_date(year: int, month: int, day: int) -> date:
    # Handle leap-day anniversaries in non-leap years by celebrating on Feb 28.
    try:
        return date(year, month, day)
    except ValueError:
        if month == 2 and day == 29:
            return date(year, 2, 28)
        raise
