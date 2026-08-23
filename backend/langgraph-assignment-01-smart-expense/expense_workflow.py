"""LangGraph Smart Expense Processing Workflow.

The workflow simulates a company expense approval system:
1. Receive an expense amount in USD.
2. Add 10% tax.
3. Convert the final taxed amount to INR.
4. Route approval based on the original USD amount.
"""

from __future__ import annotations

from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph


TAX_RATE = 0.10
DEFAULT_USD_TO_INR_RATE = 83.0


class ExpenseState(TypedDict, total=False):
    """State passed between LangGraph nodes."""

    expense_usd: float
    tax_usd: float
    total_usd: float
    conversion_rate: float
    converted_inr: float
    approval_route: str
    decision: str
    trace: list[str]


def _get_trace(state: ExpenseState) -> list[str]:
    """Return a copied trace list so nodes do not mutate state in place."""
    return list(state.get("trace", []))


def add_tax(state: ExpenseState) -> ExpenseState:
    """Add 10% tax to the original USD expense."""
    expense_usd = float(state["expense_usd"])
    tax_usd = round(expense_usd * TAX_RATE, 2)
    total_usd = round(expense_usd + tax_usd, 2)

    trace = _get_trace(state)
    trace.append(f"Added 10% tax: ${expense_usd:.2f} + ${tax_usd:.2f} = ${total_usd:.2f}")

    return {
        "tax_usd": tax_usd,
        "total_usd": total_usd,
        "trace": trace,
    }


def convert_to_inr(state: ExpenseState) -> ExpenseState:
    """Convert the taxed USD amount to INR using a fixed conversion rate."""
    total_usd = float(state["total_usd"])
    conversion_rate = float(state.get("conversion_rate", DEFAULT_USD_TO_INR_RATE))
    converted_inr = round(total_usd * conversion_rate, 2)

    trace = _get_trace(state)
    trace.append(
        f"Converted taxed amount to INR: ${total_usd:.2f} * {conversion_rate:.2f} = INR {converted_inr:.2f}"
    )

    return {
        "converted_inr": converted_inr,
        "trace": trace,
    }


def route_by_original_amount(state: ExpenseState) -> Literal["auto", "manager", "finance"]:
    """Route based on the original submitted USD amount."""
    expense_usd = float(state["expense_usd"])

    if expense_usd <= 100:
        return "auto"
    if expense_usd <= 1000:
        return "manager"
    return "finance"


def auto_approved(state: ExpenseState) -> ExpenseState:
    """Approve small expenses automatically."""
    trace = _get_trace(state)
    trace.append("Routing decision: amount <= 100 USD, so the expense is Auto Approved.")
    return {
        "approval_route": "auto",
        "decision": "Auto Approved",
        "trace": trace,
    }


def manager_approval(state: ExpenseState) -> ExpenseState:
    """Route medium expenses to the manager."""
    trace = _get_trace(state)
    trace.append("Routing decision: 100 < amount <= 1000 USD, so Manager Approval is required.")
    return {
        "approval_route": "manager",
        "decision": "Manager Approval",
        "trace": trace,
    }


def finance_approval(state: ExpenseState) -> ExpenseState:
    """Route large expenses to the finance department."""
    trace = _get_trace(state)
    trace.append("Routing decision: amount > 1000 USD, so Finance Department Approval is required.")
    return {
        "approval_route": "finance",
        "decision": "Finance Department Approval",
        "trace": trace,
    }


def build_expense_graph():
    """Build and compile the LangGraph workflow."""
    graph = StateGraph(ExpenseState)

    graph.add_node("add_tax", add_tax)
    graph.add_node("convert_to_inr", convert_to_inr)
    graph.add_node("auto_approved", auto_approved)
    graph.add_node("manager_approval", manager_approval)
    graph.add_node("finance_approval", finance_approval)

    graph.add_edge(START, "add_tax")
    graph.add_edge("add_tax", "convert_to_inr")
    graph.add_conditional_edges(
        "convert_to_inr",
        route_by_original_amount,
        {
            "auto": "auto_approved",
            "manager": "manager_approval",
            "finance": "finance_approval",
        },
    )
    graph.add_edge("auto_approved", END)
    graph.add_edge("manager_approval", END)
    graph.add_edge("finance_approval", END)

    return graph.compile()


def process_expense(
    expense_usd: float,
    conversion_rate: float = DEFAULT_USD_TO_INR_RATE,
) -> ExpenseState:
    """Run the compiled graph for a submitted expense amount."""
    if expense_usd < 0:
        raise ValueError("Expense amount cannot be negative.")

    app = build_expense_graph()
    initial_state: ExpenseState = {
        "expense_usd": float(expense_usd),
        "conversion_rate": float(conversion_rate),
        "trace": [f"Received expense amount: ${expense_usd:.2f}"],
    }
    return app.invoke(initial_state)


def format_result(result: ExpenseState) -> str:
    """Format final workflow output for console printing."""
    return (
        "Smart Expense Processing Result\n"
        "--------------------------------\n"
        f"Original Amount USD: ${result['expense_usd']:.2f}\n"
        f"Tax Added USD: ${result['tax_usd']:.2f}\n"
        f"Final Amount USD: ${result['total_usd']:.2f}\n"
        f"Converted Amount INR: INR {result['converted_inr']:.2f}\n"
        f"Final Decision: {result['decision']}"
    )


def print_trace(result: ExpenseState) -> None:
    """Print the workflow trace and final output."""
    print("Workflow Trace")
    print("--------------")
    for step_number, step in enumerate(result.get("trace", []), start=1):
        print(f"Step {step_number}: {step}")
    print()
    print(format_result(result))
