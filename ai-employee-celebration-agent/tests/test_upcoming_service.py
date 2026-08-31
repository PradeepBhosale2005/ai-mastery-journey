from datetime import date

from src.actual_report_client import ActualReportEmployee
from src.upcoming_service import find_planned_celebrations, planned_to_table


def _employee(**overrides):
    data = {
        "employee_id": "21001",
        "preferred_name": "Logan McNeil",
        "legal_first_name": "Logan",
        "legal_last_name": "McNeil",
        "email": "logan@example.com",
        "manager_email": "manager@example.com",
        "status": "Active",
        "country": "United States of America",
        "next_birthday_date": date(2027, 5, 25),
        "original_hire_date": date(2000, 1, 1),
        "supervisory_organization": "Human Resources",
        "timezone_raw": "GMT-08:00 Pacific Time (Los Angeles)",
        "timezone": "America/Los_Angeles",
    }
    data.update(overrides)
    return ActualReportEmployee(**data)


def test_upcoming_service_finds_birthday_inside_window():
    planned = find_planned_celebrations([_employee()], date(2027, 5, 1), lookahead_days=30)

    assert len(planned) == 1
    assert planned[0].event.event_type == "birthday"
    assert planned[0].days_until == 24


def test_upcoming_service_finds_due_today_birthday():
    planned = find_planned_celebrations([_employee()], date(2027, 5, 25), lookahead_days=30)

    assert len(planned) == 1
    assert planned[0].is_today is True
    assert planned[0].priority_label == "Due Today"


def test_upcoming_service_finds_anniversary():
    planned = find_planned_celebrations([_employee()], date(2027, 1, 1), lookahead_days=0)

    assert len(planned) == 1
    assert planned[0].event.event_type == "work_anniversary"
    assert planned[0].event.years == 27


def test_upcoming_service_skips_inactive_employee():
    planned = find_planned_celebrations([_employee(status="Inactive")], date(2027, 5, 25), lookahead_days=30)

    assert planned == []


def test_planned_to_table_returns_ui_rows():
    planned = find_planned_celebrations([_employee()], date(2027, 5, 25), lookahead_days=30)
    rows = planned_to_table(planned)

    assert rows[0]["Name"] == "Logan McNeil"
    assert rows[0]["Event Type"] == "Birthday"
    assert rows[0]["Priority"] == "Due Today"
