"""
Run the Article Analysis System with the company Llama API using a longer timeout.

This version is useful when the Llama server is slow or the model takes longer
than 60 seconds to respond.

Environment variables used:
- LLAMA_BASE_URL
- LLAMA_MODEL
- LLAMA_VERIFY_SSL
- LLAMA_USERNAME
- LLAMA_PASSWORD
- LLAMA_TIMEOUT, optional, default 180 seconds

Do not save real usernames or passwords in this file or in GitHub.
"""

import argparse
import json
import os
from typing import Any, Dict

import requests
import urllib3

from article_analyzer import (
    LLMAPIError,
    analyze_article_from_raw_response,
    build_prompt,
    extract_text_from_api_response,
    format_analysis_as_json,
)


def parse_bool(value: str | None, default: bool = True) -> bool:
    """Convert common string values into a boolean."""
    if value is None:
        return default
    return value.strip().lower() in {"true", "1", "yes", "y"}


def parse_timeout(value: str | None, default: int = 180) -> int:
    """Read timeout seconds from environment variable."""
    if value is None:
        return default

    try:
        timeout = int(value)
    except ValueError:
        return default

    return max(timeout, 30)


def build_llama_chat_completions_url(base_url: str) -> str:
    """Build the OpenAI-compatible chat completions URL from LLAMA_BASE_URL."""
    base_url = base_url.rstrip("/")

    if base_url.endswith("/chat/completions"):
        return base_url

    return f"{base_url}/chat/completions"


def build_llama_payload(prompt: str, model: str) -> Dict[str, Any]:
    """Build an OpenAI-compatible payload for the Llama API."""
    return {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are a precise assistant that returns only valid JSON.",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
    }


def call_llama_api(prompt: str) -> str:
    """Call the company Llama API and return the raw model response text."""
    base_url = os.getenv("LLAMA_BASE_URL")
    model = os.getenv("LLAMA_MODEL", "llama3.1:8b")
    username = os.getenv("LLAMA_USERNAME")
    password = os.getenv("LLAMA_PASSWORD")
    verify_ssl = parse_bool(os.getenv("LLAMA_VERIFY_SSL"), default=True)
    timeout = parse_timeout(os.getenv("LLAMA_TIMEOUT"), default=180)

    if not base_url:
        raise LLMAPIError("LLAMA_BASE_URL is not configured.")

    if not verify_ssl:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    api_url = build_llama_chat_completions_url(base_url)
    payload = build_llama_payload(prompt, model)
    headers = {"Content-Type": "application/json"}

    auth = None
    if username and password:
        auth = (username, password)

    try:
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            auth=auth,
            verify=verify_ssl,
            timeout=timeout,
        )
        response.raise_for_status()
        response_json = response.json()
    except requests.exceptions.Timeout as exc:
        raise LLMAPIError(
            f"Llama API request timed out after {timeout} seconds. "
            "Try again, reduce the article length, or ask the API owner if the server is busy."
        ) from exc
    except requests.exceptions.RequestException as exc:
        raise LLMAPIError(f"Llama API request failed: {exc}") from exc
    except ValueError as exc:
        raise LLMAPIError("Llama API response was not valid JSON.") from exc

    return extract_text_from_api_response(response_json)


def analyze_article_with_llama(article: str) -> Dict[str, Any]:
    """Analyze an article using the company Llama API."""
    if not article or not article.strip():
        raise ValueError("Article text cannot be empty.")

    prompt = build_prompt(article)
    raw_response = call_llama_api(prompt)
    return analyze_article_from_raw_response(raw_response)


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze an article using the company Llama API.")
    parser.add_argument("article_file", help="Path to the text file containing the article")
    parser.add_argument(
        "--output",
        default="llama_analysis_output.json",
        help="Path where the JSON analysis output should be saved",
    )

    args = parser.parse_args()

    try:
        with open(args.article_file, "r", encoding="utf-8") as file:
            article = file.read()

        analysis = analyze_article_with_llama(article)
        formatted_json = format_analysis_as_json(analysis)

        print(formatted_json)

        with open(args.output, "w", encoding="utf-8") as file:
            json.dump(analysis, file, indent=2, ensure_ascii=False)

        print(f"\nAnalysis saved to: {args.output}")

    except Exception as exc:
        print("Article analysis failed.")
        print(f"Error: {exc}")


if __name__ == "__main__":
    main()
