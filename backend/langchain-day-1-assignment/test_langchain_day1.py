"""Lightweight tests for LangChain Day-1 assignment files.

These tests avoid live LLM calls so they can run even when external APIs or
Ollama are unavailable.
"""

import unittest

from assignment1_messy_data_cleaner import PROMPT as ASSIGNMENT1_PROMPT
from assignment2_marketing_assembly_line import SLOGAN_PROMPT, TRANSLATION_PROMPT
from assignment3_mini_rag import QUESTION, retrieve_rules
from assignment4_token_receipt import ApproxTokenCallbackHandler
from local_embeddings import HashEmbeddings


class TestLangChainDay1(unittest.TestCase):
    def test_assignment1_prompt_uses_required_variable_and_format(self):
        self.assertIn("messy_review", ASSIGNMENT1_PROMPT.input_variables)
        prompt_text = ASSIGNMENT1_PROMPT.template
        self.assertIn("Sentiment:", prompt_text)
        self.assertIn("Core Issue:", prompt_text)

    def test_assignment2_prompts_support_lcel_flow(self):
        self.assertIn("product_name", SLOGAN_PROMPT.input_variables)
        self.assertIn("slogan", TRANSLATION_PROMPT.input_variables)
        self.assertIn("Exactly 5 words", SLOGAN_PROMPT.template)
        self.assertIn("French", TRANSLATION_PROMPT.template)

    def test_hash_embeddings_are_deterministic(self):
        embeddings = HashEmbeddings(dimensions=32)
        first = embeddings.embed_query("golden token")
        second = embeddings.embed_query("golden token")
        self.assertEqual(first, second)
        self.assertEqual(len(first), 32)

    def test_mini_rag_retrieves_golden_token_rule(self):
        docs = retrieve_rules(QUESTION)
        combined = " ".join(doc.page_content for doc in docs).lower()
        self.assertIn("golden token", combined)
        self.assertIn("50", combined)

    def test_callback_token_counter(self):
        counter = ApproxTokenCallbackHandler(cost_per_1000_tokens=0.01)
        self.assertGreater(counter.estimate_tokens("hello world!"), 0)


if __name__ == "__main__":
    unittest.main()
