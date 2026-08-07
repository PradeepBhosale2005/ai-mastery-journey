"""Interaction orchestration with tolerant JSON parsing and relevance validation."""

from typing import Any, Dict

from logger_utils import InteractionLogger
from prompts import (
    build_model_a_final_prompt,
    build_model_a_initial_prompt,
    build_model_b_critique_prompt,
    build_synthesis_prompt,
)
from validators_lenient import (
    parse_json_object,
    validate_final_result,
    validate_relevance,
    validate_structured_response,
)


class MultiModelInteractionSystem:
    """Coordinate a structured discussion between two LLM models."""

    def __init__(self, model_a_client: Any, model_b_client: Any, log_path: str = "logs/interaction_log.jsonl") -> None:
        self.model_a_client = model_a_client
        self.model_b_client = model_b_client
        self.logger = InteractionLogger(log_path)

    def _call_model_for_response(self, client: Any, turn: str, prompt: str, topic: str) -> str:
        """Call a model, log prompt and raw output, parse JSON, and validate relevance."""
        model_name = getattr(client, "name", "unknown_model")

        self.logger.log_prompt(turn=turn, model_name=model_name, prompt=prompt)

        try:
            raw_output = client.complete(prompt)
            self.logger.log_raw_output(turn=turn, model_name=model_name, raw_output=raw_output)

            parsed = parse_json_object(raw_output)
            response_text = validate_structured_response(parsed, field_name="response")
            validate_relevance(response_text, topic)
            return response_text
        except Exception as exc:
            self.logger.log_error(turn=turn, model_name=model_name, error_message=str(exc))
            raise

    def _call_model_for_conclusion(self, client: Any, turn: str, prompt: str, topic: str) -> str:
        """Call a model for the final synthesized conclusion."""
        model_name = getattr(client, "name", "unknown_model")

        self.logger.log_prompt(turn=turn, model_name=model_name, prompt=prompt)

        try:
            raw_output = client.complete(prompt)
            self.logger.log_raw_output(turn=turn, model_name=model_name, raw_output=raw_output)

            parsed = parse_json_object(raw_output)
            conclusion = validate_structured_response(parsed, field_name="conclusion")
            validate_relevance(conclusion, topic)
            return conclusion
        except Exception as exc:
            self.logger.log_error(turn=turn, model_name=model_name, error_message=str(exc))
            raise

    def run_interaction(self, topic: str) -> Dict[str, str]:
        """Run A -> B -> A interaction and produce the final JSON-ready result."""
        if not topic or not topic.strip():
            raise ValueError("Topic cannot be empty.")

        topic = topic.strip()

        model_a_initial_prompt = build_model_a_initial_prompt(topic)
        model_a_initial_response = self._call_model_for_response(
            client=self.model_a_client,
            turn="A_INITIAL",
            prompt=model_a_initial_prompt,
            topic=topic,
        )

        model_b_prompt = build_model_b_critique_prompt(topic, model_a_initial_response)
        model_b_critique_response = self._call_model_for_response(
            client=self.model_b_client,
            turn="B_CRITIQUE",
            prompt=model_b_prompt,
            topic=topic,
        )

        model_a_final_prompt = build_model_a_final_prompt(
            topic,
            model_a_initial_response,
            model_b_critique_response,
        )
        model_a_final_reply = self._call_model_for_response(
            client=self.model_a_client,
            turn="A_FINAL",
            prompt=model_a_final_prompt,
            topic=topic,
        )

        synthesis_prompt = build_synthesis_prompt(
            topic,
            model_a_initial_response,
            model_b_critique_response,
            model_a_final_reply,
        )
        synthesized_conclusion = self._call_model_for_conclusion(
            client=self.model_b_client,
            turn="SYNTHESIS",
            prompt=synthesis_prompt,
            topic=topic,
        )

        final_result = {
            "topic": topic,
            "model_a_initial_response": model_a_initial_response,
            "model_b_critique_response": model_b_critique_response,
            "model_a_final_reply": model_a_final_reply,
            "synthesized_conclusion": synthesized_conclusion,
        }

        return validate_final_result(final_result)
