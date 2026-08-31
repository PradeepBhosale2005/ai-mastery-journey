from datetime import date

from src.actual_report_client import ActualReportEmployee
from src.delivery_service import APIPostSettings, OperationalDeliveryService, SMTPSettings
from src.upcoming_service import find_planned_celebrations


def _planned_event():
    employee = ActualReportEmployee(
        employee_id="21001",
        preferred_name="Logan McNeil",
        legal_first_name="Logan",
        legal_last_name="McNeil",
        email="logan@example.com",
        manager_email="manager@example.com",
        status="Active",
        country="United States of America",
        next_birthday_date=date(2027, 5, 25),
        original_hire_date=date(2000, 1, 1),
        supervisory_organization="Human Resources",
        timezone_raw="GMT-08:00 Pacific Time (Los Angeles)",
        timezone="America/Los_Angeles",
    )
    return find_planned_celebrations([employee], date(2027, 5, 25), lookahead_days=30)[0]


def test_delivery_service_records_outbox_and_dry_run_channels(tmp_path):
    service = OperationalDeliveryService(
        outbox_path=tmp_path / "outbox.jsonl",
        smtp_settings=SMTPSettings(
            enabled=False,
            host="smtp.example.com",
            port=587,
            username="",
            password="",
            from_email="agent@example.com",
            from_name="Agent",
            use_tls=True,
            use_ssl=False,
            to_override="test@example.com",
            cc_list=[],
            cc_manager=False,
        ),
        api_settings=APIPostSettings(
            enabled=False,
            url="https://example.com/hook",
            method="POST",
            bearer_token="",
            headers={},
            timeout_seconds=30,
        ),
    )

    results = service.deliver(
        planned=_planned_event(),
        message="Happy Birthday!",
        run_id="test-run",
        dry_run=True,
        send_email=True,
        post_api=True,
    )

    assert [result["channel"] for result in results] == ["jsonl_outbox", "smtp_email", "generic_api"]
    assert results[0]["status"] == "RECORDED"
    assert results[1]["status"] == "DRY_RUN"
    assert results[2]["status"] == "DRY_RUN"
    assert (tmp_path / "outbox.jsonl").exists()
