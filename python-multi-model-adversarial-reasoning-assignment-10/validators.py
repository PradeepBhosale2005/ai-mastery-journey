"""Validation helpers for adversarial model responses and final output."""

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
    "this",
    "that",
    "should",
    "must",
    "can",
    "will",
}


EXPANDED_KEYWORDS = {
    "ai": {"ai", "artificial", "intelligence", "machine", "algorithm", "automation"},
    "education": {"education", "learning", "teaching", "student", "students", "school", "classroom"},
    "business": {"business", "market", "customer", "customers", "revenue", "cost", "proposal"},
    "policy": {"policy", "rule", "governance", "compliance", "regulation", "risk"},
    "technical": {"technical", "system", "design", "architecture", "implementation", "security"},
}


FINAL_KEYS = {
    "original_input",
    "model_a_initial_proposal",
    "model_b_critique",
    "model_a_revised_response",
    "final_evaluation",
}


def clean_possible_json_wrapper(raw_response: str) -> str:
    """Remove common accidental wrappers around JSON."""
    text = raw_response.strip()

    if text.startswith("```") and text.endswith("```"):
        text = re.sub(r"^```(?:json)?", "", text, flags=re.IGNORECASE).strip()
        text = re.sub(r"```$", "", text).strip()

    if text.startswith("`") and text.endswith("`"):
        text = text[1:-1].strip()

    return text


def parse_json_object(raw_response: str) -> Dict[str, Any]:
    """Parse raw model output as a JSON object."""
    text = clean_possible_json_wrapper(raw_response)

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as first_error:
        start = text.find("{")
        end = text.rfind("}")

        if start != -1 and end != -1 and end > start:
            try:
                parsed = json.loads(text[start : end + 1])
            except json.JSONDecodeError as second_error:
                raise ValidationError("Model output must be valid JSON.") from second_error
        else:
            raise ValidationError("Model output must be valid JSON.") from first_error

    if not isinstance(parsed, dict):
        raise ValidationError("Model output must be a JSON object.")

    return parsed


def validate_turn_response(data: Dict[str, Any], field_name: str = "response") -> str:
    """Validate a structured model response and return its text field."""
    if set(data.keys()) != {field_name}:
        raise ValidationError(f"Model JSON must contain only the field: {field_name}")

    response_text = data[field_name]

    if not isinstance(response_text, str) or not response_text.strip():
        raise ValidationError(f"{field_name} must be a non-empty string.")

    return response_text.strip()


def input_keywords(user_input: str) -> Set[str]:
    """Return relevant keywords from the original user input."""
    words = re.findall(r"[a-zA-Z0-9]+", user_input.lower())
    keywords = {word for word in words if word not in STOPWORDS and len(word) > 2}

    expanded = set(keywords)
    for keyword in keywords:
        expanded.update(EXPANDED_KEYWORDS.get(keyword, set()))

    return expanded


def validate_relevance(text: str, user_input: str) -> None:
    """Validate that a response appears relevant to the original scenario."""
    keywords = input_keywords(user_input)

    if not keywords:
        return

    text_words = set(re.findall(r"[a-zA-Z0-9]+", text.lower()))

    if keywords.intersection(text_words):
        return

    text_lower = text.lower()
    if any(keyword in text_lower for keyword in keywords if len(keyword) > 3):
        return

    raise ValidationError("Response does not appear relevant to the original input.")


def validate_final_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """Validate final assignment JSON schema and content."""
    if set(result.keys()) != FINAL_KEYS:
        raise ValidationError("Final output does not match the required JSON schema.")

    for key in FINAL_KEYS:
        if not isinstance(result[key], str) or not result[key].strip():
            raise ValidationError(f"{key} must be a non-empty string.")

    original_input = result["original_input"]
    validate_relevance(result["model_a_initial_proposal"], original_input)
    validate_relevance(result["model_b_critique"], original_input)
    validate_relevance(result["model_a_revised_response"], original_input)
    validate_relevance(result["final_evaluation"], original_input)

    return result
