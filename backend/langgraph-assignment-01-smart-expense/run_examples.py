"""Run all required routing examples for the Smart Expense workflow."""

from __future__ import annotations

from expense_workflow import format_result, process_expense


EXAMPLE_AMOUNTS = [50.0, 500.0, 1500.0]


def main() -> None:
    for amount in EXAMPLE_AMOUNTS:
        result = process_expense(amount)
        print("=" * 70)
        print(format_result(result))
        print()


if __name__ == "__main__":
    main()
