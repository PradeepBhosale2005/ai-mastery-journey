"""
Diagnose company-hosted Model A and Model B API configuration.

This script loads local_model_config.txt and checks whether the configured
server supports common endpoints:

1. OpenAI-compatible:
   - GET  /v1/models
   - POST /v1/chat/completions

2. Ollama-style:
   - GET  /api/tags
   - POST /api/chat

The script does not print passwords or secrets.
"""

import json
import os
from typing import Optional, Tuple

import requests
import urllib3

from config_loader import load_local_config
from llm_client import parse_bool, parse_timeout


def short_text(value: str, limit: int = 700) -> str:
    """Return a short one-line response preview."""
    value = value.replace("\n", " ").replace("\r", " ")
    if len(value) > limit:
        return value[:limit] + "..."
    return value


def get_root_url(base_url: str) -> str:
    """Return server root URL by removing a trailing /v1 if present."""
    base_url = base_url.rstrip("/")
    if base_url.endswith("/v1"):
        return base_url[:-3].rstrip("/")
    return base_url


def build_auth(username: Optional[str], password: Optional[str]) -> Optional[Tuple[str, str]]:
    """Build basic auth tuple only when both username and password are available."""
    if username and password:
        return (username, password)
    return None


def request_get(label: str, url: str, auth, verify_ssl: bool, timeout: int) -> None:
    """Run a GET request and print status plus a response preview."""
    try:
        response = requests.get(url, auth=auth, verify=verify_ssl, timeout=timeout)
        print(f"{label}: {response.status_code} {response.reason}")
        print(short_text(response.text))
    except Exception as exc:
        print(f"{label}: FAILED")
        print(exc)
    print("-" * 80)


def request_post(label: str, url: str, payload: dict, auth, verify_ssl: bool, timeout: int) -> None:
    """Run a POST request and print status plus a response preview."""
    try:
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json=payload,
            auth=auth,
            verify=verify_ssl,
            timeout=timeout,
        )
        print(f"{label}: {response.status_code} {response.reason}")
        print(short_text(response.text))
    except Exception as exc:
        print(f"{label}: FAILED")
        print(exc)
    print("-" * 80)


def diagnose(prefix: str, model_label: str) -> None:
    """Diagnose one model config prefix such as MODEL_A or MODEL_B."""
    base_url = os.getenv(f"{prefix}_BASE_URL")
    model = os.getenv(f"{prefix}_MODEL")
    username = os.getenv(f"{prefix}_USERNAME")
    password = os.getenv(f"{prefix}_PASSWORD")
    verify_ssl = parse_bool(os.getenv(f"{prefix}_VERIFY_SSL"), default=True)
    timeout = parse_timeout(os.getenv(f"{prefix}_TIMEOUT"), default=60)

    print("=" * 80)
    print(f"Diagnosing {model_label} ({prefix})")
    print(f"Base URL: {base_url}")
    print(f"Model: {model}")
    print(f"SSL verification: {verify_ssl}")
    print(f"Timeout: {timeout}")
    print("Password printed: no")
    print("=" * 80)

    if not base_url or not model:
        print(f"Missing {prefix}_BASE_URL or {prefix}_MODEL in local_model_config.txt")
        print()
        return

    if not verify_ssl:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    auth = build_auth(username, password)
    base_url = base_url.rstrip("/")
    root_url = get_root_url(base_url)

    openai_models_url = f"{base_url}/models"
    openai_chat_url = f"{base_url}/chat/completions"
    ollama_tags_url = f"{root_url}/api/tags"
    ollama_chat_url = f"{root_url}/api/chat"

    openai_payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": "Return only JSON: {\"response\": \"hello\"}"}
        ],
        "temperature": 0.2,
    }

    ollama_payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": "Return only JSON: {\"response\": \"hello\"}"}
        ],
        "stream": False,
        "options": {"temperature": 0.2},
    }

    request_get("OpenAI models endpoint", openai_models_url, auth, verify_ssl, timeout)
    request_post("OpenAI chat completions endpoint", openai_chat_url, openai_payload, auth, verify_ssl, timeout)
    request_get("Ollama tags endpoint", ollama_tags_url, auth, verify_ssl, timeout)
    request_post("Ollama chat endpoint", ollama_chat_url, ollama_payload, auth, verify_ssl, timeout)


def main() -> None:
    load_local_config("local_model_config.txt")
    diagnose("MODEL_A", "Model A")
    diagnose("MODEL_B", "Model B")


if __name__ == "__main__":
    main()
