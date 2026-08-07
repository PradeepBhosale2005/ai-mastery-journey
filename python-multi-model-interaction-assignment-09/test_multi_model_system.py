"""Unit tests for the Multi-Model Interaction System."""

import json
import tempfile
import unittest
from pathlib import Path

from mock_models import MockModelClient
from orchestrator import MultiModelInteractionSystem
from prompts import (
    build_model_a_final_prompt,
    build_model_a_initial_prompt,
    build_model_b_critique_prompt,
)
from validators import (
    ValidationError,
    parse_json_object,
    validate_final_result,
    validate_relevance,
    validate_structured_response,
)


class TestMultiModelInteractionSystem(unittest.TestCase):
    def test_prompt_builders_include_topic_and_json_instruction(self):
        topic = "AI in education"
        prompt_a = build_model_a_initial_prompt(topic)
        prompt_b = build_model_b_critique_prompt(topic, "Model A response")
        prompt_final = build_model_a_final_prompt(topic, "A response", "B response")

        self.assertIn(topic, prompt_a)
        self.assertIn(topic, prompt_b)
        self.assertIn(topic, prompt_final)
        self.assertIn("valid JSON", prompt_a)
        self.assertIn("valid JSON", prompt_b)
        self.assertIn("valid JSON", prompt_final)

    def test_parse_and_validate_structured_response(self):
        parsed = parse_json_object('{"response": "AI in education can support personalized learning."}')
        text = validate_structured_response(parsed)

        self.assertEqual(text, "AI in education can support personalized learning.")

    def test_invalid_json_is_rejected(self):
        with self.assertRaises(ValidationError):
            parse_json_object("Here is the answer: {not json}")

    def test_relevance_validation(self):
        validate_relevance("AI in education improves feedback.", "AI in education")

        with self.assertRaises(ValidationError):
            validate_relevance("This response discusses gardening only.", "AI in education")

    def test_mock_interaction_returns_required_final_json(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            log_path = str(Path(temp_dir) / "interaction_log.jsonl")
            system = MultiModelInteractionSystem(
                MockModelClient("Model A"),
                MockModelClient("Model B"),
                log_path=log_path,
            )

            result = system.run_interaction("AI in education")
            validate_final_result(result)

            self.assertEqual(result["topic"], "AI in education")
            self.assertIn("AI in education", result["model_a_initial_response"])
            self.assertIn("AI in education", result["model_b_critique_response"])
            self.assertIn("AI in education", result["model_a_final_reply"])
            self.assertIn("AI in education", result["synthesized_conclusion"])

            log_content = Path(log_path).read_text(encoding="utf-8")
            self.assertIn("A_INITIAL", log_content)
            self.assertIn("B_CRITIQUE", log_content)
            self.assertIn("A_FINAL", log_content)
            self.assertIn("SYNTHESIS", log_content)

    def test_final_json_can_be_serialized(self):
        result = {
            "topic": "AI in education",
            "model_a_initial_response": "AI in education can improve learning outcomes.",
            "model_b_critique_response": "AI in education also needs privacy and fairness safeguards.",
            "model_a_final_reply": "AI in education should be implemented with safeguards.",
            "synthesized_conclusion": "AI in education is useful when balanced with safeguards.",
        }

        validated = validate_final_result(result)
        serialized = json.dumps(validated)
        self.assertIn("AI in education", serialized)


if __name__ == "__main__":
    unittest.main()
