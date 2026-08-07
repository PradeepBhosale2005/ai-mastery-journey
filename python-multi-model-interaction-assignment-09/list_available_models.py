"""
List available model names from the configured company model server.

This helps when a configured model name returns:
model '...' not found

The script loads local_model_config.txt and calls the OpenAI-compatible
/models endpoint. It can also filter the output by a search term.

Examples:
python list_available_models.py
python list_available_models.py deepseek
python list_available_models.py qwen
"""

import argparse
import os
from typing import Any, Dict, List

import requests
import urllib3

from config_loader import load_local_config
from llm_client import parse_bool, parse_timeout


def get_models_url(base_url: str) -> str:
    """Build /models endpoint from a base URL."""
    base_url = base_url.rstrip("/")
    if base_url.endswith("/models"):
        return base_url
    return f"{base_url}/models"


def extract_model_names(response_json: Dict[str, Any]) -> List[str]:
    """Extract model names from OpenAI-compatible or Ollama-style model lists."""
    names: List[str] = []

    if "data" in response_json and isinstance(response_json["data"], list):
        for item in response_json["data"]:
            if isinstance(item, dict) and "id" in item:
                names.append(str(item["id"]))

    if "models" in response_json and isinstance(response_json["models"], list):
        for item in response_json["models"]:
            if isinstance(item, dict):
                name = item.get("name") or item.get("model")
                if name:
                    names.append(str(name))

    return sorted(set(names), key=str.lower)


def list_models(prefix: str, filter_text: str | None) -> None:
    """List models for MODEL_A or MODEL_B configuration."""
    base_url = os.getenv(f"{prefix}_BASE_URL")
    username = os.getenv(f"{prefix}_USERNAME")
    password = os.getenv(f"{prefix}_PASSWORD")
    verify_ssl = parse_bool(os.getenv(f"{prefix}_VERIFY_SSL"), default=True)
    timeout = parse_timeout(os.getenv(f"{prefix}_TIMEOUT"), default=60)

    print("=" * 80)
    print(f"Checking {prefix}")
    print(f"Base URL: {base_url}")
    print("Password printed: no")
    print("=" * 80)

    if not base_url:
        print(f"{prefix}_BASE_URL is missing in local_model_config.txt")
        return

    if not verify_ssl:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    auth = None
    if username and password:
        auth = (username, password)

    try:
        response = requests.get(
            get_models_url(base_url),
            auth=auth,
            verify=verify_ssl,
            timeout=timeout,
        )
        response.raise_for_status()
        response_json = response.json()
    except Exception as exc:
        print(f"Failed to fetch model list: {exc}")
        return

    names = extract_model_names(response_json)

    if filter_text:
        filtered = [name for name in names if filter_text.lower() in name.lower()]
    else:
        filtered = names

    if not filtered:
        print(f"No models matched filter: {filter_text}")
        print("Available model count:", len(names))
        print("First 25 available models:")
        for name in names[:25]:
            print("-", name)
        return

    print(f"Matching models ({len(filtered)}):")
    for name in filtered:
        print("-", name)


def main() -> None:
    parser = argparse.ArgumentParser(description="List available company-hosted model names.")
    parser.add_argument(
        "filter",
        nargs="?",
        default=None,
        help="Optional text filter, for example deepseek, qwen, llama, gpt",
    )

    args = parser.parse_args()

    load_local_config("local_model_config.txt")
    list_models("MODEL_A", args.filter)
    list_models("MODEL_B", args.filter)


if __name__ == "__main__":
    main()
