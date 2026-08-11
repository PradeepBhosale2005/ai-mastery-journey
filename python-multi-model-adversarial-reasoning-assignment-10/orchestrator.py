"""Orchestration for Model A -> Model B -> Model A adversarial reasoning."""

from typing import Any, Dict

from logger_utils import InteractionLogger
from prompt_builder import (
    build_final_evaluation_prompt,
    build_model_a_initial_prompt,
    build_model_a_revision_prompt,
    build_model_b_critique_prompt,
)
from validators import (
    parse_json_object,
    validate_final_result,
    validate_relevance,
    validate_turn_response,
)


class AdversarialReasoningSystem:
    """Coordinate adversarial reasoning between two model clients."""

    def __init__(
        self,
        model_a_client: Any,
        model_b_client: Any,
        log_path: str = "logs/adversarial_log.jsonl",
    ) -> None:
        self.model_a_client = model_a_client
        self.model_b_client = model_b_client
        self.logger = InteractionLogger(log_path)

    def _call_response_turn(self, client: Any, turn: str, prompt: str, original_input: str) -> str:
        """Call one model response turn, log everything, and validate output."""
        model_name = getattr(client, "name", "unknown_model")
        self.logger.log_prompt(turn=turn, model_name=model_name, prompt=prompt)

        try:
            raw_output = client.complete(prompt)
            self.logger.log_raw_output(turn=turn, model_name=model_name, raw_output=raw_output)

            parsed = parse_json_object(raw_output)
            response_text = validate_turn_response(parsed, field_name="response")
            validate_relevance(response_text, original_input)
            return response_text
        except Exception as exc:
            self.logger.log_error(turn=turn, model_name=model_name, error_message=str(exc))
            raise

    def _call_evaluation_turn(self, client: Any, turn: str, prompt: str, original_input: str) -> str:
        """Call final evaluation turn, log everything, and validate output."""
        model_name = getattr(client, "name", "unknown_model")
        self.logger.log_prompt(turn=turn, model_name=model_name, prompt=prompt)

        try:
            raw_output = client.complete(prompt)
            self.logger.log_raw_output(turn=turn, model_name=model_name, raw_output=raw_output)

            parsed = parse_json_object(raw_output)
            evaluation = validate_turn_response(parsed, field_name="evaluation")
            validate_relevance(evaluation, original_input)
            return evaluation
        except Exception as exc:
            self.logger.log_error(turn=turn, model_name=model_name, error_message=str(exc))
            raise

    def run(self, original_input: str) -> Dict[str, str]:
        """Run the full adversarial reasoning workflow."""
        if not original_input or not original_input.strip():
            raise ValueError("Original input cannot be empty.")

        original_input = original_input.strip()

        model_a_initial_prompt = build_model_a_initial_prompt(original_input)
        model_a_initial_proposal = self._call_response_turn(
            client=self.model_a_client,
            turn="A_INITIAL_PROPOSAL",
            prompt=model_a_initial_prompt,
            original_input=original_input,
        )

        model_b_critique_prompt = build_model_b_critique_prompt(
            original_input,
            model_a_initial_proposal,
        )
        model_b_critique = self._call_response_turn(
            client=self.model_b_client,
            turn="B_ADVERSARIAL_CRITIQUE",
            prompt=model_b_critique_prompt,
            original_input=original_input,
        )

        model_a_revision_prompt = build_model_a_revision_prompt(
            original_input,
            model_a_initial_proposal,
            model_b_critique,
        )
        model_a_revised_response = self._call_response_turn(
            client=self.model_a_client,
            turn="A_REVISED_RESPONSE",
            prompt=model_a_revision_prompt,
            original_input=original_input,
        )

        final_evaluation_prompt = build_final_evaluation_prompt(
            original_input,
            model_a_initial_proposal,
            model_b_critique,
            model_a_revised_response,
        )
        final_evaluation = self._call_evaluation_turn(
            client=self.model_b_client,
            turn="FINAL_EVALUATION",
            prompt=final_evaluation_prompt,
            original_input=original_input,
        )

        final_result = {
            "original_input": original_input,
            "model_a_initial_proposal": model_a_initial_proposal,
            "model_b_critique": model_b_critique,
            "model_a_revised_response": model_a_revised_response,
            "final_evaluation": final_evaluation,
        }

        return validate_final_result(final_result)
