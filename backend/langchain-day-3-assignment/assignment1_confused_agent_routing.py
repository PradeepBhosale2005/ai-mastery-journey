"""Assignment 1: The Confused Agent Routing Challenge.

The agent selects between two similar financial tools by reading precise tool
docstrings. The routing decision is not implemented with manual if/else logic;
the local agent scores the user's request against the tool documentation, and the
optional live LLM path asks the model to choose using the same docstrings.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Dict, List

from langchain_core.messages import HumanMessage
from langchain_core.tools import StructuredTool

from llm_factory import get_llm, use_live_llm
from tools import ROUTING_TOOLS, ToolCall, tool_description, tool_registry


CANCEL_TEST = "I don't want to use your software anymore, stop charging john@email.com."
REFUND_TEST = "My last charge of $50 on ID #TXN991 was a mistake, give it back."

STOP_WORDS = {
    "a", "an", "and", "are", "for", "from", "i", "is", "it", "my", "of", "on", "or",
    "the", "this", "to", "use", "was", "with", "your"
}


@dataclass
class AgentRun:
    """Trace for a single routing run."""

    prompt: str
    selected_tool: str
    argument_name: str
    argument_value: str
    result: str


def _tokens(text: str) -> set[str]:
    """Tokenize text for docstring-based local routing."""
    return {
        token
        for token in re.findall(r"[a-zA-Z0-9]+", text.lower())
        if token not in STOP_WORDS and len(token) > 1
    }


def _score_tool(user_prompt: str, tool: StructuredTool) -> int:
    """Score how well a user's language matches a tool's docstring."""
    prompt_tokens = _tokens(user_prompt)
    documentation_tokens = _tokens(tool.name + " " + tool.description)
    return len(prompt_tokens.intersection(documentation_tokens))


def route_with_docstrings(user_prompt: str, tools: List[StructuredTool]) -> str:
    """Select a tool using only tool names and docstrings as routing evidence."""
    scores = {tool.name: _score_tool(user_prompt, tool) for tool in tools}
    return max(scores, key=scores.get)


def _extract_email(text: str) -> str:
    """Extract the first email address from text."""
    match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    if not match:
        raise ValueError("No email address found for cancel_subscription.")
    return match.group(0)


def _extract_transaction_id(text: str) -> str:
    """Extract a transaction id like TXN991 from text."""
    match = re.search(r"#?([A-Z]{2,}\d+)", text, flags=re.IGNORECASE)
    if not match:
        raise ValueError("No transaction id found for refund_order.")
    return match.group(1).upper()


ARGUMENT_EXTRACTORS = {
    "cancel_subscription": ("email", _extract_email),
    "refund_order": ("transaction_id", _extract_transaction_id),
}


def build_router_prompt(user_prompt: str, tools: List[StructuredTool]) -> str:
    """Build an LLM prompt that exposes only tool documentation for routing."""
    tool_text = "\n\n".join(tool_description(tool) for tool in tools)
    return f"""You are a SaaS billing support agent.
Choose exactly one tool based only on the tool descriptions/docstrings.
Do not use manual rules. Return only valid JSON.

Available tools:
{tool_text}

User request:
{user_prompt}

Return JSON in this exact shape:
{{"tool_name": "refund_order or cancel_subscription"}}
"""


def route_with_llm(user_prompt: str, tools: List[StructuredTool]) -> str:
    """Ask a live LLM to select a tool using the docstring prompt."""
    llm = get_llm(temperature=0.0)
    response = llm.invoke([HumanMessage(content=build_router_prompt(user_prompt, tools))])
    raw_text = str(response.content).strip()
    parsed = json.loads(raw_text)
    tool_name = parsed["tool_name"]
    if tool_name not in {tool.name for tool in tools}:
        raise ValueError(f"LLM selected unknown tool: {tool_name}")
    return tool_name


def build_tool_call(user_prompt: str, selected_tool: str) -> ToolCall:
    """Extract the required argument for the selected tool."""
    argument_name, extractor = ARGUMENT_EXTRACTORS[selected_tool]
    return ToolCall(
        tool_name=selected_tool,
        argument_name=argument_name,
        argument_value=extractor(user_prompt),
    )


def run_agent(user_prompt: str, live_llm: bool | None = None) -> AgentRun:
    """Run the routing agent and execute the selected tool."""
    if live_llm is None:
        live_llm = use_live_llm(default=False)

    selected_tool = (
        route_with_llm(user_prompt, ROUTING_TOOLS)
        if live_llm
        else route_with_docstrings(user_prompt, ROUTING_TOOLS)
    )
    tool_call = build_tool_call(user_prompt, selected_tool)
    registry: Dict[str, StructuredTool] = tool_registry(ROUTING_TOOLS)
    result = registry[tool_call.tool_name].invoke({tool_call.argument_name: tool_call.argument_value})

    return AgentRun(
        prompt=user_prompt,
        selected_tool=tool_call.tool_name,
        argument_name=tool_call.argument_name,
        argument_value=tool_call.argument_value,
        result=result,
    )


def print_run(run: AgentRun) -> None:
    """Print one routing result clearly."""
    print(f"User Prompt: {run.prompt}")
    print(f"Selected Tool: {run.selected_tool}")
    print(f"Tool Argument: {run.argument_name}={run.argument_value}")
    print(f"Tool Result: {run.result}")
    print()


def main() -> None:
    """Run both required test cases."""
    print("Assignment 1: Confused Agent Routing Challenge")
    print("Routing evidence comes from tool names and docstrings.\n")
    print_run(run_agent(CANCEL_TEST))
    print_run(run_agent(REFUND_TEST))


if __name__ == "__main__":
    main()
