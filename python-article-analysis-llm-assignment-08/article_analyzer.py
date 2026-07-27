"""
Article Analysis System using a company-hosted LLM API.

The system:
1. Accepts an article as input.
2. Builds a strict JSON-only prompt.
3. Sends the prompt to a configurable company-hosted LLM API.
4. Parses and validates the JSON response.
5. Handles API failures and malformed responses gracefully.
"""

import json
import os
from typing import Any, Dict, List

import requests


REQUIRED_KEYS = {"summary", "important_points", "key_themes", "target_audience"}


class ArticleAnalysisError(Exception):
    """Base exception for article analysis errors."""


class LLMAPIError(ArticleAnalysisError):
    """Raised when the LLM API call fails."""


class ResponseValidationError(ArticleAnalysisError):
    """Raised when the LLM response is invalid or does not follow the schema."""


def count_words(text: str) -> int:
    """Return the number of words in a text string."""
    return len(text.split())


def build_prompt(article: str) -> str:
    """Build a strict prompt for article analysis."""
    return f"""
You are an Article Analysis System.
Analyze the article provided below and return the output strictly as a valid JSON object.

Rules:
1. Do not include markdown, code fences, explanations, or any text outside the JSON object.
2. The JSON object must contain exactly these fields:
   - summary
   - important_points
   - key_themes
   - target_audience
3. The summary must be concise and limited to 150 words.
4. important_points must be an array containing 5 to 10 clear strings.
5. key_themes must be an array containing 3 to 5 short phrases, not full sentences.
6. target_audience must briefly identify the most relevant audience for the article.

Required JSON format:
{{
  "summary": "summary within 150 words",
  "important_points": [
    "point 1",
    "point 2",
    "point 3",
    "point 4",
    "point 5"
  ],
  "key_themes": [
    "theme 1",
    "theme 2",
    "theme 3"
  ],
  "target_audience": "brief audience description"
}}

Article:
{article}
""".strip()


def build_api_payload(prompt: str, model: str | None = None) -> Dict[str, Any]:
    """
    Build a generic OpenAI-compatible chat payload.

    If the company-hosted LLM API expects a different payload structure,
    update only this function.
    """
    payload: Dict[str, Any] = {
        "messages": [
            {
                "role": "system",
                "content": "You are a precise assistant that returns only valid JSON.",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
    }

    if model:
        payload["model"] = model

    return payload


def extract_text_from_api_response(response_json: Dict[str, Any]) -> str:
    """
    Extract the LLM text from common company/OpenAI-style API response formats.

    Supported formats:
    1. Direct JSON object with required fields.
    2. OpenAI-style choices[0].message.content.
    3. choices[0].text.
    4. output_text, content, or response fields.
    """
    if REQUIRED_KEYS.issubset(response_json.keys()):
        return json.dumps(response_json)

    if "choices" in response_json and response_json["choices"]:
        first_choice = response_json["choices"][0]

        if "message" in first_choice and "content" in first_choice["message"]:
            return first_choice["message"]["content"]

        if "text" in first_choice:
            return first_choice["text"]

    for key in ["output_text", "content", "response"]:
        if key in response_json and isinstance(response_json[key], str):
            return response_json[key]

    raise ResponseValidationError("Unable to extract JSON text from the LLM API response.")


def call_company_llm_api(prompt: str, api_url: str, api_key: str | None, model: str | None = None) -> str:
    """Call the company-hosted LLM API and return the raw model response text."""
    headers = {"Content-Type": "application/json"}

    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    payload = build_api_payload(prompt, model)

    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        response_json = response.json()
    except requests.exceptions.RequestException as exc:
        raise LLMAPIError(f"LLM API request failed: {exc}") from exc
    except ValueError as exc:
        raise LLMAPIError("LLM API response was not valid JSON.") from exc

    return extract_text_from_api_response(response_json)


def parse_json_response(raw_response: str) -> Dict[str, Any]:
    """Parse a raw model response as strict JSON."""
    cleaned_response = raw_response.strip()

    try:
        parsed = json.loads(cleaned_response)
    except json.JSONDecodeError as exc:
        raise ResponseValidationError(
            "Malformed LLM response. The response must contain only a valid JSON object."
        ) from exc

    if not isinstance(parsed, dict):
        raise ResponseValidationError("LLM response must be a JSON object.")

    return parsed


def validate_analysis_json(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate the article analysis JSON structure and assignment constraints."""
    keys = set(data.keys())

    if keys != REQUIRED_KEYS:
        missing = REQUIRED_KEYS - keys
        extra = keys - REQUIRED_KEYS
        raise ResponseValidationError(
            f"JSON fields are invalid. Missing fields: {missing}. Extra fields: {extra}."
        )

    summary = data["summary"]
    important_points = data["important_points"]
    key_themes = data["key_themes"]
    target_audience = data["target_audience"]

    if not isinstance(summary, str) or not summary.strip():
        raise ResponseValidationError("summary must be a non-empty string.")

    if count_words(summary) > 150:
        raise ResponseValidationError("summary must be limited to 150 words.")

    if not isinstance(important_points, list):
        raise ResponseValidationError("important_points must be an array of strings.")

    if not 5 <= len(important_points) <= 10:
        raise ResponseValidationError("important_points must contain 5 to 10 items.")

    if not all(isinstance(point, str) and point.strip() for point in important_points):
        raise ResponseValidationError("Each important point must be a non-empty string.")

    if not isinstance(key_themes, list):
        raise ResponseValidationError("key_themes must be an array of strings.")

    if not 3 <= len(key_themes) <= 5:
        raise ResponseValidationError("key_themes must contain 3 to 5 items.")

    for theme in key_themes:
        if not isinstance(theme, str) or not theme.strip():
            raise ResponseValidationError("Each key theme must be a non-empty string.")
        if count_words(theme) > 8:
            raise ResponseValidationError("Each key theme should be a short phrase, not a full sentence.")

    if not isinstance(target_audience, str) or not target_audience.strip():
        raise ResponseValidationError("target_audience must be a non-empty string.")

    return data


def analyze_article_from_raw_response(raw_response: str) -> Dict[str, Any]:
    """Parse and validate a raw LLM response string."""
    parsed_response = parse_json_response(raw_response)
    return validate_analysis_json(parsed_response)


def analyze_article(
    article: str,
    api_url: str | None = None,
    api_key: str | None = None,
    model: str | None = None,
) -> Dict[str, Any]:
    """Analyze an article using the configured company-hosted LLM API."""
    if not article or not article.strip():
        raise ValueError("Article text cannot be empty.")

    api_url = api_url or os.getenv("COMPANY_LLM_API_URL")
    api_key = api_key or os.getenv("COMPANY_LLM_API_KEY")
    model = model or os.getenv("COMPANY_LLM_MODEL")

    if not api_url:
        raise LLMAPIError("COMPANY_LLM_API_URL is not configured.")

    prompt = build_prompt(article)
    raw_response = call_company_llm_api(prompt, api_url, api_key, model)
    return analyze_article_from_raw_response(raw_response)


def format_analysis_as_json(data: Dict[str, Any]) -> str:
    """Return formatted JSON for display or saving."""
    return json.dumps(data, indent=2, ensure_ascii=False)
