from __future__ import annotations

import json

from dotenv import load_dotenv

from src.real_workday_client import RealWorkdayRaaSClient


def main() -> None:
    load_dotenv()
    client = RealWorkdayRaaSClient.from_env()
    employees = client.get_all_employees()

    print("Real Workday connection successful.")
    print(f"Employees fetched: {len(employees)}")

    preview = []
    for employee in employees[:5]:
        preview.append(
            {
                "employee_id": employee.employee_id,
                "worker_id": employee.worker_id,
                "preferred_name": employee.preferred_name,
                "email_present": bool(employee.email),
                "date_of_birth_present": bool(employee.date_of_birth),
                "hire_date_present": bool(employee.hire_date),
                "timezone": employee.timezone,
                "status": employee.status,
                "celebration_channel": employee.celebration_channel,
            }
        )

    print(json.dumps(preview, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
