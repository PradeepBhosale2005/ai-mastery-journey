"""Tests for the LangGraph Smart Expense Processing workflow."""

from __future__ import annotations

import unittest

from expense_workflow import (
    DEFAULT_USD_TO_INR_RATE,
    build_expense_graph,
    format_result,
    process_expense,
    route_by_original_amount,
)


class TestSmartExpenseWorkflow(unittest.TestCase):
    def test_graph_builds(self) -> None:
        app = build_expense_graph()
        self.assertIsNotNone(app)

    def test_auto_approval_route(self) -> None:
        result = process_expense(100.0)
        self.assertEqual(result["decision"], "Auto Approved")
        self.assertEqual(result["tax_usd"], 10.0)
        self.assertEqual(result["total_usd"], 110.0)
        self.assertEqual(result["converted_inr"], round(110.0 * DEFAULT_USD_TO_INR_RATE, 2))

    def test_manager_approval_route(self) -> None:
        result = process_expense(500.0)
        self.assertEqual(result["decision"], "Manager Approval")
        self.assertEqual(result["tax_usd"], 50.0)
        self.assertEqual(result["total_usd"], 550.0)

    def test_finance_approval_route(self) -> None:
        result = process_expense(1500.0)
        self.assertEqual(result["decision"], "Finance Department Approval")
        self.assertEqual(result["tax_usd"], 150.0)
        self.assertEqual(result["total_usd"], 1650.0)

    def test_route_boundaries(self) -> None:
        self.assertEqual(route_by_original_amount({"expense_usd": 100.0}), "auto")
        self.assertEqual(route_by_original_amount({"expense_usd": 100.01}), "manager")
        self.assertEqual(route_by_original_amount({"expense_usd": 1000.0}), "manager")
        self.assertEqual(route_by_original_amount({"expense_usd": 1000.01}), "finance")

    def test_custom_conversion_rate(self) -> None:
        result = process_expense(200.0, conversion_rate=80.0)
        self.assertEqual(result["total_usd"], 220.0)
        self.assertEqual(result["converted_inr"], 17600.0)

    def test_negative_amount_rejected(self) -> None:
        with self.assertRaises(ValueError):
            process_expense(-1.0)

    def test_format_result_contains_decision_and_inr(self) -> None:
        result = process_expense(50.0)
        output = format_result(result)
        self.assertIn("Final Decision: Auto Approved", output)
        self.assertIn("Converted Amount INR", output)


if __name__ == "__main__":
    unittest.main()
