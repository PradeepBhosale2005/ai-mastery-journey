"""Unit tests for the Multi-Model Adversarial Reasoning System."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from llm_client import LLMClient, parse_bool, parse_int
from mock_models import MockModelClient
from orchestrator import AdversarialReasoningSystem
from prompt_builder import (
    build_model_a_initial_prompt,
    build_model_a_revision_prompt,
    build_model_b_critique_prompt,
)
from validators import (
    ValidationError,
    parse_json_object,
    validate_final_result,
    validate_relevance,
    validate_turn_response,
)


class TestAdversarialReasoningSystem(unittest.TestCase):
    def test_prompt_builders_include_original_input_and_context(self):
        scenario = "AI assistant for customer support"
        initial = "Initial proposal"
        critique = "Critique response"

        prompt_a = build_model_a_initial_prompt(scenario)
        prompt_b = build_model_b_critique_prompt(scenario, initial)
        prompt_revision = build_model_a_revision_prompt(scenario, initial, critique)

        self.assertIn(scenario, prompt_a)
        self.assertIn(scenario, prompt_b)
        self.assertIn(scenario, prompt_revision)
        self.assertIn(initial, prompt_b)
        self.assertIn(critique, prompt_revision)
        self.assertIn("valid JSON", prompt_a)

    def test_parse_json_object_and_turn_response(self):
        parsed = parse_json_object('{"response": "AI assistant proposal for customer support."}')
        response = validate_turn_response(parsed)

        self.assertEqual(response, "AI assistant proposal for customer support.")

    def test_invalid_json_is_rejected(self):
        with self.assertRaises(ValidationError):
            parse_json_object("not json")

    def test_relevance_validation_accepts_related_terms(self):
        validate_relevance(
            "The artificial intelligence assistant improves learning support for students.",
            "AI in education",
        )

        with self.assertRaises(ValidationError):
            validate_relevance("This response is about cooking recipes only.", "AI in education")

    def test_mock_adversarial_interaction_returns_required_json(self):
        scenario = "AI assistant for customer support"

        with tempfile.TemporaryDirectory() as temp_dir:
            log_path = str(Path(temp_dir) / "adversarial_log.jsonl")
            system = AdversarialReasoningSystem(
                MockModelClient("Model A"),
                MockModelClient("Model B"),
                log_path=log_path,
            )

            result = system.run(scenario)
            validate_final_result(result)

            self.assertEqual(result["original_input"], scenario)
            self.assertIn("customer support", result["model_a_initial_proposal"])
            self.assertIn("customer support", result["model_b_critique"])
            self.assertIn("customer support", result["model_a_revised_response"])
            self.assertIn("customer support", result["final_evaluation"])

            log_content = Path(log_path).read_text(encoding="utf-8")
            self.assertIn("A_INITIAL_PROPOSAL", log_content)
            self.assertIn("B_ADVERSARIAL_CRITIQUE", log_content)
            self.assertIn("A_REVISED_RESPONSE", log_content)
            self.assertIn("FINAL_EVALUATION", log_content)

    def test_final_json_can_be_serialized(self):
        result = {
            "original_input": "AI assistant for customer support",
            "model_a_initial_proposal": "The AI assistant supports customer support with faster responses.",
            "model_b_critique": "The customer support AI assistant has privacy and accuracy risks.",
            "model_a_revised_response": "The AI assistant adds safeguards for customer support quality.",
            "final_evaluation": "The customer support AI assistant is stronger but still needs governance.",
        }

        validated = validate_final_result(result)
        serialized = json.dumps(validated)
        self.assertIn("customer support", serialized)

    def test_retry_client_retries_on_server_error(self):
        client = LLMClient(
            name="Model A",
            base_url="https://example.com/v1",
            model="test-model",
            timeout=30,
            retries=1,
            retry_delay=0,
        )

        first_response = Mock(status_code=500)
        first_response.raise_for_status.side_effect = Exception("server error")
        second_response = Mock(status_code=200)
        second_response.json.return_value = {
            "choices": [
                {"message": {"content": '{"response": "AI customer support response"}'}}
            ]
        }
        second_response.raise_for_status.return_value = None

        with patch("llm_client.requests.post", side_effect=[first_response, second_response]) as mocked_post:
            output = client.complete("test prompt")

        self.assertEqual(output, '{"response": "AI customer support response"}')
        self.assertEqual(mocked_post.call_count, 2)

    def test_parse_helpers(self):
        self.assertFalse(parse_bool("false"))
        self.assertTrue(parse_bool("true"))
        self.assertEqual(parse_int("10", default=2, minimum=0), 10)
        self.assertEqual(parse_int("bad", default=2, minimum=0), 2)


if __name__ == "__main__":
    unittest.main()
