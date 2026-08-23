"""Command-line runner for the LangGraph Smart Expense workflow."""

from __future__ import annotations

import argparse

from expense_workflow import DEFAULT_USD_TO_INR_RATE, print_trace, process_expense


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Smart Expense LangGraph workflow.")
    parser.add_argument(
        "amount",
        nargs="?",
        type=float,
        default=250.0,
        help="Expense amount in USD. Default: 250.0",
    )
    parser.add_argument(
        "--rate",
        type=float,
        default=DEFAULT_USD_TO_INR_RATE,
        help=f"USD to INR conversion rate. Default: {DEFAULT_USD_TO_INR_RATE}",
    )
    args = parser.parse_args()

    result = process_expense(args.amount, conversion_rate=args.rate)
    print_trace(result)


if __name__ == "__main__":
    main()
