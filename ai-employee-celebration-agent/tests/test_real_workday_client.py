from src.real_workday_client import RealWorkdayRaaSClient


def test_real_workday_client_maps_report_entry_rows() -> None:
    payload = {
        "Report_Entry": [
            {
                "Employee_ID": "E900",
                "Worker_ID": "W900",
                "Preferred_Name": "Real Demo",
                "Legal_Name": "Real Demo Legal",
                "Work_Email": "real.demo@example.com",
                "Manager_Email": "manager@example.com",
                "Date_of_Birth": "1995-08-29",
                "Hire_Date": "2020-08-29",
                "Time_Zone": "Asia/Kolkata",
                "Country": "India",
                "Department": "HR Operations",
                "Worker_Status": "Active",
                "Celebration_Channel": "Email",
            }
        ]
    }

    client = RealWorkdayRaaSClient(raas_url="https://example.invalid/report")
    employees = client.rows_to_employees(payload)

    assert len(employees) == 1
    employee = employees[0]
    assert employee.employee_id == "E900"
    assert employee.worker_id == "W900"
    assert employee.preferred_name == "Real Demo"
    assert employee.email == "real.demo@example.com"
    assert employee.is_active is True
    assert employee.timezone == "Asia/Kolkata"


def test_real_workday_client_supports_custom_field_map() -> None:
    payload = {
        "data": [
            {
                "EmpNo": "E901",
                "WorkerNo": "W901",
                "FirstName": "Custom Demo",
                "OfficeEmail": "custom.demo@example.com",
                "BirthDate": "1990-08-29",
                "StartDate": "2019-08-29",
                "EmpStatus": "Active",
            }
        ]
    }

    client = RealWorkdayRaaSClient(
        raas_url="https://example.invalid/report",
        field_candidates={
            "employee_id": ["EmpNo"],
            "worker_id": ["WorkerNo"],
            "preferred_name": ["FirstName"],
            "legal_name": ["FirstName"],
            "email": ["OfficeEmail"],
            "manager_email": [],
            "date_of_birth": ["BirthDate"],
            "hire_date": ["StartDate"],
            "timezone": [],
            "country": [],
            "department": [],
            "status": ["EmpStatus"],
            "celebration_channel": [],
        },
    )
    employees = client.rows_to_employees(payload)

    assert employees[0].employee_id == "E901"
    assert employees[0].preferred_name == "Custom Demo"
    assert employees[0].email == "custom.demo@example.com"
