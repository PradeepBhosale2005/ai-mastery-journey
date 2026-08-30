from __future__ import annotations

import json

from dotenv import load_dotenv

from src.actual_report_client import ActualWorkdayReportClient


def main() -> None:
    load_dotenv()
    client = ActualWorkdayReportClient.from_env()
    employees = client.get_all_employees()

    print("Actual Workday report connection successful.")
    print(f"Employees fetched: {len(employees)}")

    preview = [employee.preview_dict() for employee in employees[:5]]
    print(json.dumps(preview, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
