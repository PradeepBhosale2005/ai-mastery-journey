from datetime import date

from src.celebration_detector import CelebrationDetector
from src.models import Employee


def test_detector_finds_birthday_and_anniversary_for_active_employees() -> None:
    employees = [
        Employee.from_dict(
            {
                "employee_id": "E100",
                "worker_id": "W100",
                "preferred_name": "Test Birthday",
                "legal_name": "Test Birthday",
                "email": "birthday@example.com",
                "manager_email": "manager@example.com",
                "date_of_birth": "1995-08-29",
                "hire_date": "2024-01-01",
                "timezone": "Asia/Kolkata",
                "country": "India",
                "department": "Engineering",
                "status": "Active",
                "celebration_channel": "Email",
            }
        ),
        Employee.from_dict(
            {
                "employee_id": "E101",
                "worker_id": "W101",
                "preferred_name": "Test Anniversary",
                "legal_name": "Test Anniversary",
                "email": "anniversary@example.com",
                "manager_email": "manager@example.com",
                "date_of_birth": "1992-03-01",
                "hire_date": "2020-08-29",
                "timezone": "Asia/Kolkata",
                "country": "India",
                "department": "HR",
                "status": "Active",
                "celebration_channel": "Jadean Jar",
            }
        ),
    ]

    events = CelebrationDetector().find_events(employees, date(2026, 8, 29))
    assert len(events) == 2
    assert {event.event_type for event in events} == {"birthday", "work_anniversary"}


def test_detector_skips_inactive_employee() -> None:
    employee = Employee.from_dict(
        {
            "employee_id": "E102",
            "worker_id": "W102",
            "preferred_name": "Inactive User",
            "legal_name": "Inactive User",
            "email": "inactive@example.com",
            "manager_email": "manager@example.com",
            "date_of_birth": "1995-08-29",
            "hire_date": "2020-08-29",
            "timezone": "Asia/Kolkata",
            "country": "India",
            "department": "Finance",
            "status": "Inactive",
            "celebration_channel": "Email",
        }
    )

    events = CelebrationDetector().find_events([employee], date(2026, 8, 29))
    assert events == []
