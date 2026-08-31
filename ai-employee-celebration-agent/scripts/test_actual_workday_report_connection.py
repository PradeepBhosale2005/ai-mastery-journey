from __future__ import annotations

import json
import sys
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.actual_report_client import ActualWorkdayReportClient


def main() -> None:
    load_dotenv(PROJECT_ROOT / ".env")
    client = ActualWorkdayReportClient.from_env()
    employees = client.get_all_employees()

    print("Actual Workday report connection successful.")
    print(f"Employees fetched: {len(employees)}")

    preview = [employee.preview_dict() for employee in employees[:5]]
    print(json.dumps(preview, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
