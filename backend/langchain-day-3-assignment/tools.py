"""Custom tools for LangChain Day-3 assignments."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List

from langchain_core.tools import StructuredTool


# Assignment 1 tools -------------------------------------------------------

def refund_order(transaction_id: str) -> str:
    """Use ONLY to refund, return, reverse, or give back money from a specific past charge, order, invoice, or transaction. This tool is for one-time historical payment mistakes such as a last charge being wrong. It requires a transaction_id like TXN991 and must not be used to stop future subscription billing."""
    cleaned_id = transaction_id.strip().replace("#", "")
    return f"Refund initiated for transaction {cleaned_id}."


def cancel_subscription(email: str) -> str:
    """Use ONLY to cancel a recurring subscription, stop future charges, stop charging a customer, end software access, or prevent future billing. This tool is for ongoing subscriptions and requires the customer's email address. It must not be used to refund a past transaction or give money back for a completed charge."""
    cleaned_email = email.strip().lower()
    return f"Subscription canceled for {cleaned_email}. Future recurring charges are stopped."


REFUND_TOOL = StructuredTool.from_function(refund_order)
CANCEL_TOOL = StructuredTool.from_function(cancel_subscription)
ROUTING_TOOLS: List[StructuredTool] = [REFUND_TOOL, CANCEL_TOOL]


# Assignment 2 tools -------------------------------------------------------

def get_internal_stock_price(ticker: str) -> str:
    """Primary internal stock price database lookup. This is the preferred first source for stock prices, but in this exercise it intentionally fails to simulate a database outage."""
    return f"Error: Database Timeout while retrieving price for {ticker.upper()} from internal stock database."


def search_public_web(query: str) -> str:
    """Backup public web search tool. Use this only after the internal stock price database fails. It retrieves mock public financial information and cannot access private internal databases."""
    normalized_query = query.lower()
    if "apple" in normalized_query or "aapl" in normalized_query:
        return "Apple stock is at $170."
    return "Mock public web result: no specific stock price found."


INTERNAL_STOCK_TOOL = StructuredTool.from_function(get_internal_stock_price)
PUBLIC_WEB_TOOL = StructuredTool.from_function(search_public_web)
RESILIENCE_TOOLS: List[StructuredTool] = [INTERNAL_STOCK_TOOL, PUBLIC_WEB_TOOL]


@dataclass(frozen=True)
class ToolCall:
    """A selected tool call used by the local docstring-guided agent."""

    tool_name: str
    argument_name: str
    argument_value: str


def tool_description(tool: StructuredTool) -> str:
    """Return the text the agent sees for a tool."""
    return f"Tool: {tool.name}\nDescription: {tool.description}\nArgs: {tool.args}"


def tool_registry(tools: List[StructuredTool]) -> Dict[str, StructuredTool]:
    """Build a name-to-tool registry for executing selected actions."""
    return {tool.name: tool for tool in tools}
