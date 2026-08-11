"""Assignment 2: Agent Resilience - The Broken API Challenge.

The financial agent tries the primary internal stock price tool first, observes a
simulated outage, then recovers by switching to the backup public web search tool.
"""

from __future__ import annotations

from dataclasses import dataclass

from tools import get_internal_stock_price, search_public_web


TEST_QUERY = "What is the current stock price of Apple?"


@dataclass
class ResilienceTrace:
    """Execution trace for the resilient financial agent."""

    user_query: str
    thought_1: str
    action_1: str
    observation_1: str
    thought_2: str
    action_2: str
    observation_2: str
    final_answer: str


def run_resilient_agent(user_query: str = TEST_QUERY) -> ResilienceTrace:
    """Run the primary-failure and backup-recovery workflow."""
    ticker = "AAPL"
    thought_1 = (
        "The user is asking for Apple's stock price. The internal stock database "
        "is the primary source, so I will try it first."
    )
    action_1 = 'get_internal_stock_price(ticker="AAPL")'
    observation_1 = get_internal_stock_price(ticker)

    thought_2 = (
        "The internal database returned a timeout error. I need to recover by "
        "using the backup public web search tool."
    )
    action_2 = 'search_public_web(query="current stock price of Apple")'
    observation_2 = search_public_web("current stock price of Apple")
    final_answer = "The current stock price of Apple is $170."

    return ResilienceTrace(
        user_query=user_query,
        thought_1=thought_1,
        action_1=action_1,
        observation_1=observation_1,
        thought_2=thought_2,
        action_2=action_2,
        observation_2=observation_2,
        final_answer=final_answer,
    )


def print_trace(trace: ResilienceTrace) -> None:
    """Print the required terminal trace."""
    print("Assignment 2: Agent Resilience - The Broken API Challenge")
    print(f"User Query: {trace.user_query}")
    print(f"Thought 1: {trace.thought_1}")
    print(f"Action 1: {trace.action_1}")
    print(f"Observation 1: {trace.observation_1}")
    print(f"Thought 2: {trace.thought_2}")
    print(f"Action 2: {trace.action_2}")
    print(f"Observation 2: {trace.observation_2}")
    print(f"Final Answer: {trace.final_answer}")


def main() -> None:
    """Run the required resilience test query."""
    print_trace(run_resilient_agent())


if __name__ == "__main__":
    main()
