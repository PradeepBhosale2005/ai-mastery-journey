"""Local tests for LangChain Day-2 assignment code.

These tests do not make live LLM or external API calls.
"""

import unittest

from assignment1_self_correcting_agent import run_agent
from assignment2_smart_splitter import CHUNK_OVERLAP, extract_overlap, split_document
from assignment3_context_poisoning import load_policy_documents, retrieve_policy
from assignment4_fast_grounded_cache import GROUNDING_FAILURE, answer_question
from tools import calculate_expression, search_fact


class TestLangChainDay2(unittest.TestCase):
    def test_calculator_tool_math(self) -> None:
        self.assertEqual(calculate_expression("1879 * 5"), "9395")
        self.assertEqual(calculate_expression("10 + 5"), "15")
        self.assertEqual(calculate_expression("20 / 4"), "5")

    def test_search_tool_finds_einstein_birth_year(self) -> None:
        self.assertEqual(search_fact("Albert Einstein birth year"), "1879")

    def test_self_correcting_agent_final_answer(self) -> None:
        trace = run_agent(use_llm=False)
        self.assertEqual(trace["observation_1"], "1879")
        self.assertEqual(trace["final_answer"], "9395")

    def test_smart_splitter_overlap(self) -> None:
        text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" * 20
        chunks = split_document(text)
        self.assertGreaterEqual(len(chunks), 2)
        overlap = extract_overlap(chunks[0], chunks[1])
        self.assertEqual(len(overlap), CHUNK_OVERLAP)
        self.assertTrue(chunks[1].startswith(overlap))

    def test_policy_documents_have_expected_metadata(self) -> None:
        documents = load_policy_documents()
        years = {doc.metadata["year"] for doc in documents}
        self.assertEqual(years, {2022, 2024})

    def test_metadata_filter_retrieves_only_2024_policy(self) -> None:
        document = retrieve_policy("What is the WFH policy?", 2024)
        self.assertEqual(document.metadata["year"], 2024)
        self.assertIn("allowed 3 days", document.page_content)
        self.assertNotIn("strictly banned", document.page_content)

    def test_grounded_cache_and_failure_message(self) -> None:
        cache = {}
        answer_1, from_cache_1 = answer_question(
            "What is the WFH policy?", cache=cache, use_llm=False
        )
        answer_2, from_cache_2 = answer_question(
            "What is the WFH policy?", cache=cache, use_llm=False
        )
        answer_3, from_cache_3 = answer_question(
            "What is the recipe for a chocolate cake?", cache=cache, use_llm=False
        )

        self.assertFalse(from_cache_1)
        self.assertTrue(from_cache_2)
        self.assertEqual(answer_1, answer_2)
        self.assertFalse(from_cache_3)
        self.assertEqual(answer_3, GROUNDING_FAILURE)


if __name__ == "__main__":
    unittest.main()
