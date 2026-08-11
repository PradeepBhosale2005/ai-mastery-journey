"""Local tests for LangChain Day-3 assignment code.

These tests do not make live LLM or external API calls.
"""

import unittest

from assignment1_confused_agent_routing import CANCEL_TEST, REFUND_TEST, run_agent
from assignment2_agent_resilience import run_resilient_agent
from assignment3_lost_context_rag import (
    EXPECTED_ANSWER,
    QUESTION,
    generate_answer,
    retrieve_context,
    run_rag_pipeline,
    split_document,
)
from tools import cancel_subscription, get_internal_stock_price, refund_order, search_public_web


class TestLangChainDay3(unittest.TestCase):
    def test_refund_tool(self) -> None:
        self.assertIn("TXN991", refund_order("TXN991"))

    def test_cancel_tool(self) -> None:
        self.assertIn("john@email.com", cancel_subscription("john@email.com"))

    def test_confused_agent_routes_cancel(self) -> None:
        run = run_agent(CANCEL_TEST, live_llm=False)
        self.assertEqual(run.selected_tool, "cancel_subscription")
        self.assertEqual(run.argument_value, "john@email.com")

    def test_confused_agent_routes_refund(self) -> None:
        run = run_agent(REFUND_TEST, live_llm=False)
        self.assertEqual(run.selected_tool, "refund_order")
        self.assertEqual(run.argument_value, "TXN991")

    def test_primary_stock_tool_fails(self) -> None:
        self.assertIn("Error: Database Timeout", get_internal_stock_price("AAPL"))

    def test_backup_web_tool_returns_apple_price(self) -> None:
        self.assertIn("$170", search_public_web("current stock price of Apple"))

    def test_resilient_agent_recovers(self) -> None:
        trace = run_resilient_agent()
        self.assertIn("Database Timeout", trace.observation_1)
        self.assertIn("search_public_web", trace.action_2)
        self.assertEqual(trace.final_answer, "The current stock price of Apple is $170.")

    def test_lost_context_splitter_creates_chunks(self) -> None:
        chunks = split_document()
        self.assertGreaterEqual(len(chunks), 2)
        self.assertTrue(all("chunk_index" in chunk.metadata for chunk in chunks))

    def test_lost_context_retrieval_gets_project_and_budget(self) -> None:
        retrieved, _ = retrieve_context(QUESTION)
        context = "\n".join(document.page_content for document in retrieved)
        self.assertIn("Project Phoenix", context)
        self.assertIn("December 31st", context)
        self.assertIn("$500,000", context)

    def test_lost_context_answer_is_exact(self) -> None:
        result = run_rag_pipeline(live_llm=False)
        self.assertEqual(result.final_answer, EXPECTED_ANSWER)
        self.assertEqual(generate_answer(QUESTION, result.retrieved_chunks, live_llm=False), EXPECTED_ANSWER)


if __name__ == "__main__":
    unittest.main()
