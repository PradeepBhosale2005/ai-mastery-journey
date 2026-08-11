"""Robust validation helpers for real model outputs.

The assignment asks models to return strict JSON. Real hosted models sometimes add
markdown fences, backticks, or hidden reasoning tags. This module still validates
that the usable payload is a JSON object with the required fields, while cleaning
common wrappers so the CLI can continue running with company-hosted models.
"""

import json
import re
from typing import Any, Dict, Iterable, Optional, Set


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


EXPANDED_KEYWORDS = {
    "ai": {
        "ai",
        "artificial",
        "intelligence",
        "assistant",
        "assistants",
        "automation",
        "automated",
        "model",
        "models",
        "chatbot",
        "chatbots",
    },
    "assistant": {"assistant", "assistants", "chatbot", "chatbots", "agent", "agents"},
    "customer": {"customer", "customers", "client", "clients", "user", "users"},
    "support": {
        "support",
        "service",
        "help",
        "assistance",
        "ticket",
        "tickets",
        "agent",
        "agents",
        "resolution",
    },
    "education": {
        "education",
        "educational",
        "learning",
        "teaching",
        "student",
        "students",
        "teacher",
        "teachers",
        "school",
        "schools",
        "classroom",
        "curriculum",
    },
}


FINAL_KEYS = {
    "original_input",
    "model_a_initial_proposal",
    "model_b_critique",
    "model_a_revised_response",
    "final_evaluation",
}


def _strip_common_wrappers(raw_response: str) -> str:
    """Remove common wrappers that hosted LLMs add around JSON."""
    text = raw_response.strip()

    # Qwen-style thinking blocks sometimes appear before the JSON object.
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.IGNORECASE | re.DOTALL).strip()

    # Markdown code fences: ```json ... ``` or ``` ... ```.
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE).strip()
        text = re.sub(r"\s*```$", "", text).strip()

    # Single inline-code wrapper: `{"response": "..."}`.
    if text.startswith("`") and text.endswith("`"):
        text = text[1:-1].strip()

    return text


def _balanced_json_object(text: str, start: int) -> Optional[str]:
    """Return the first balanced JSON object substring starting at start."""
    depth = 0
    in_string = False
    escaped = False

    for index in range(start, len(text)):
        char = text[index]

        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue

        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]

    return None


def _candidate_json_strings(text: str) -> Iterable[str]:
    """Yield likely JSON object strings from a raw model response."""
    cleaned = _strip_common_wrappers(text)
    yield cleaned

    for index, char in enumerate(cleaned):
        if char == "{":
            candidate = _balanced_json_object(cleaned, index)
            if candidate:
                yield candidate


def _loads_object(candidate: str) -> Dict[str, Any]:
    """Load one candidate string as a JSON object, including JSON-as-string cases."""
    parsed = json.loads(candidate)

    # Some APIs return a JSON object as an escaped string.
    if isinstance(parsed, str):
        parsed = json.loads(_strip_common_wrappers(parsed))

    if not isinstance(parsed, dict):
        raise ValidationError("Model output must be a JSON object.")

    return parsed


def parse_json_object(raw_response: str) -> Dict[str, Any]:
    """Parse raw model output into a JSON object."""
    last_error: Optional[Exception] = None

    for candidate in _candidate_json_strings(raw_response):
        try:
            return _loads_object(candidate)
        except (json.JSONDecodeError, ValidationError) as exc:
            last_error = exc

    raise ValidationError("Model output must be valid JSON.") from last_error


def validate_turn_response(data: Dict[str, Any], field_name: str = "response") -> str:
    """Validate a single model turn response and return its text field."""
    if set(data.keys()) != {field_name}:
        raise ValidationError(f"Model JSON must contain only the field: {field_name}")

    response_text = data[field_name]

    if not isinstance(response_text, str) or not response_text.strip():
        raise ValidationError(f"{field_name} must be a non-empty string.")

    return response_text.strip()


def scenario_keywords(original_input: str) -> Set[str]:
    """Return important keywords used for relevance validation."""
    words = re.findall(r"[a-zA-Z0-9]+", original_input.lower())
    keywords = {word for word in words if word not in STOPWORDS and len(word) > 1}

    expanded = set(keywords)
    for keyword in keywords:
        expanded.update(EXPANDED_KEYWORDS.get(keyword, set()))

    return expanded


def validate_relevance(text: str, original_input: str) -> None:
    """Validate that a response appears related to the scenario/problem."""
    keywords = scenario_keywords(original_input)

    if not keywords:
        return

    text_words = set(re.findall(r"[a-zA-Z0-9]+", text.lower()))
    if keywords.intersection(text_words):
        return

    text_lower = text.lower()
    if any(keyword in text_lower for keyword in keywords if len(keyword) > 3):
        return

    raise ValidationError("Response does not appear relevant to the provided input.")


def validate_final_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """Validate the final application output schema."""
    if set(result.keys()) != FINAL_KEYS:
        raise ValidationError("Final output does not match the required JSON schema.")

    for key in FINAL_KEYS:
        if not isinstance(result[key], str) or not result[key].strip():
            raise ValidationError(f"{key} must be a non-empty string.")

    validate_relevance(result["model_a_initial_proposal"], result["original_input"])
    validate_relevance(result["model_b_critique"], result["original_input"])
    validate_relevance(result["model_a_revised_response"], result["original_input"])
    validate_relevance(result["final_evaluation"], result["original_input"])

    return result
