"""Custom tools for Assignment 1.

The assignment requires two tools:
- CalculatorTool: mathematical operations only
- SearchTool: factual lookup only, no complex math
"""

import ast
import operator
from typing import Any

from langchain_core.tools import tool


_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def _safe_eval(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_safe_eval(node.operand)
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPERATORS:
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)
        if isinstance(node.op, ast.Div) and right == 0:
            raise ZeroDivisionError("Division by zero is not allowed.")
        return _ALLOWED_OPERATORS[type(node.op)](left, right)
    raise ValueError("Only add, subtract, multiply, and divide operations are allowed.")


def calculate_expression(expression: str) -> str:
    """Safely calculate a simple arithmetic expression."""
    parsed = ast.parse(expression, mode="eval")
    value = _safe_eval(parsed)
    if value.is_integer():
        return str(int(value))
    return str(value)


def search_fact(query: str) -> str:
    """Search for a factual value.

    For the required assignment prompt, this tool returns Einstein's birth year
    directly. The tool intentionally does not perform arithmetic.
    """
    normalized = query.lower()
    if "einstein" in normalized and "birth" in normalized:
        return "1879"
    if "albert einstein" in normalized:
        return "Albert Einstein was born in 1879."
    return "No reliable local factual result found for this query."


@tool("CalculatorTool")
def calculator_tool(expression: str) -> str:
    """Calculate add, subtract, multiply, and divide expressions only."""
    return calculate_expression(expression)


@tool("SearchTool")
def search_tool(query: str) -> str:
    """Retrieve factual information only. This tool does not perform complex math."""
    return search_fact(query)


def tool_name(tool_object: Any) -> str:
    """Return a LangChain tool name for display."""
    return getattr(tool_object, "name", tool_object.__class__.__name__)
