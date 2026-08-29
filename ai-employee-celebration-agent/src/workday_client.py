from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from src.models import Employee


class MockWorkdayClient:
    """Small mock client that simulates a Workday employee data API."""

    def __init__(self, data_path: str | Path = "data/mock_workday_employees.json") -> None:
        self.data_path = Path(data_path)

    def get_all_employees(self) -> list[Employee]:
        if not self.data_path.exists():
            raise FileNotFoundError(f"Mock Workday data not found: {self.data_path}")

        rows = json.loads(self.data_path.read_text(encoding="utf-8"))
        return [Employee.from_dict(row) for row in rows]

    def get_active_employees(self) -> list[Employee]:
        return [employee for employee in self.get_all_employees() if employee.is_active]


class WorkdayClientInterface:
    """Interface placeholder for a real Workday REST/SOAP client."""

    def get_all_employees(self) -> Iterable[Employee]:
        raise NotImplementedError

    def get_active_employees(self) -> Iterable[Employee]:
        raise NotImplementedError
