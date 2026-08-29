from datetime import date

from src.message_generator import CelebrationMessageGenerator
from src.models import CelebrationEvent, Employee


def _employee() -> Employee:
    return Employee.from_dict(
        {
            "employee_id": "E200",
            "worker_id": "W200",
            "preferred_name": "Sample User",
            "legal_name": "Sample User",
            "email": "sample@example.com",
            "manager_email": "manager@example.com",
            "date_of_birth": "1995-08-29",
            "hire_date": "2020-08-29",
            "timezone": "Asia/Kolkata",
            "country": "India",
            "department": "Engineering",
            "status": "Active",
            "celebration_channel": "Email",
        }
    )


def test_mock_birthday_message_contains_name() -> None:
    event = CelebrationEvent(
        employee=_employee(),
        event_type="birthday",
        celebration_date=date(1995, 8, 29),
        years=None,
        local_date=date(2026, 8, 29),
    )
    message = CelebrationMessageGenerator(provider="mock").generate(event)
    assert "Sample User" in message
    assert "Happy Birthday" in message


def test_mock_anniversary_message_contains_years() -> None:
    event = CelebrationEvent(
        employee=_employee(),
        event_type="work_anniversary",
        celebration_date=date(2020, 8, 29),
        years=6,
        local_date=date(2026, 8, 29),
    )
    message = CelebrationMessageGenerator(provider="mock").generate(event)
    assert "Sample User" in message
    assert "6 years" in message
