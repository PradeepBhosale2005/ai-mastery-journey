from datetime import date

from run_actual_workday_report_agent import find_events_from_actual_report
from src.actual_report_client import ActualWorkdayReportClient


def _sample_payload():
    return {
        "Report_Entry": [
            {
                "Active": "Active",
                "CF-LRV-Manager_Email_Id": "aa@gmail.com",
                "Country_of_position_location_on_worker_profile": "United States of America",
                "Date_of_Workers_Next_Birthday": "2027-05-25",
                "Email_-_Primary_Work_or_Primary_Home": "user@workday.net",
                "Employee_ID": "21001",
                "Legal_Name_-_First_Name": "Logan",
                "Legal_Name_-_Last_Name": "McNeil",
                "Original_Hire_Date": "2000-01-01",
                "Preferred_Name": "Logan McNeil",
                "Supervisory_Organization": "Human Resources",
                "Time_Zone_of_Location_of_Worker_s_Primary_Position": "GMT-08:00 Pacific Time (Los Angeles)",
            }
        ]
    }


def test_actual_report_client_maps_workday_fields():
    client = ActualWorkdayReportClient(report_url="https://example.com/report?format=json")
    employees = client.rows_to_employees(_sample_payload())

    assert len(employees) == 1
    employee = employees[0]
    assert employee.employee_id == "21001"
    assert employee.display_name == "Logan McNeil"
    assert employee.legal_name == "Logan McNeil"
    assert employee.email == "user@workday.net"
    assert employee.manager_email == "aa@gmail.com"
    assert employee.next_birthday_date == date(2027, 5, 25)
    assert employee.original_hire_date == date(2000, 1, 1)
    assert employee.supervisory_organization == "Human Resources"
    assert employee.timezone == "America/Los_Angeles"
    assert employee.is_active is True


def test_actual_report_event_detection_uses_exact_next_birthday():
    client = ActualWorkdayReportClient(report_url="https://example.com/report?format=json")
    employees = client.rows_to_employees(_sample_payload())

    birthday_events = find_events_from_actual_report(employees, date(2027, 5, 25))
    assert len(birthday_events) == 1
    assert birthday_events[0].event_type == "birthday"

    no_birthday_events = find_events_from_actual_report(employees, date(2026, 5, 25))
    assert no_birthday_events == []


def test_actual_report_event_detection_finds_work_anniversary():
    client = ActualWorkdayReportClient(report_url="https://example.com/report?format=json")
    employees = client.rows_to_employees(_sample_payload())

    events = find_events_from_actual_report(employees, date(2026, 1, 1))
    assert len(events) == 1
    assert events[0].event_type == "work_anniversary"
    assert events[0].years == 26
