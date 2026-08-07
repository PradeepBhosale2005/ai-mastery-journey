"""Validation helpers for model responses and final output."""

import json
import re
from typing import Any, Dict, Set


class ValidationError(Exception):
    """Raised when a response or final result fails validation."""


STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "the",
    "to",
    "with",
}


FINAL_KEYS = {
    "topic",
    "model_a_initial_response",
    "model_b_critique_response",
    "model_a_final_reply",
    "synthesized_conclusion",
}


def parse_json_object(raw_response: str) -> Dict[str, Any]:
    """Parse raw model output as a strict JSON object."""
    text = raw_response.strip()

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValidationError("Model output must be strictly valid JSON with no extra text.") from exc

    if not isinstance(parsed, dict):
        raise ValidationError("Model output must be a JSON object.")

    return parsed


def validate_structured_response(data: Dict[str, Any], field_name: str = "response") -> str:
    """Validate a model turn response and return the text field."""
    if set(data.keys()) != {field_name}:
        raise ValidationError(f"Model JSON must contain only the field: {field_name}")

    response_text = data[field_name]

    if not isinstance(response_text, str) or not response_text.strip():
        raise ValidationError(f"{field_name} must be a non-empty string.")

    return response_text.strip()


def topic_keywords(topic: str) -> Set[str]:
    """Return important topic keywords used for relevance validation."""
    words = re.findall(r"[a-zA-Z0-9]+", topic.lower())
    return {word for word in words if word not in STOPWORDS and len(word) > 2}


def validate_relevance(text: str, topic: str) -> None:
    """Validate that a response appears relevant to the topic using keyword overlap."""
    keywords = topic_keywords(topic)

    if not keywords:
        return

    text_lower = text.lower()
    if not any(keyword in text_lower for keyword in keywords):
        raise ValidationError("Response does not appear relevant to the provided topic.")


def validate_final_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """Validate the final application output schema."""
    if set(result.keys()) != FINAL_KEYS:
        raise ValidationError("Final output does not match the required JSON schema.")

    for key in FINAL_KEYS:
        if not isinstance(result[key], str) or not result[key].strip():
            raise ValidationError(f"{key} must be a non-empty string.")

    validate_relevance(result["model_a_initial_response"], result["topic"])
    validate_relevance(result["model_b_critique_response"], result["topic"])
    validate_relevance(result["model_a_final_reply"], result["topic"])
    validate_relevance(result["synthesized_conclusion"], result["topic"])

    return result
