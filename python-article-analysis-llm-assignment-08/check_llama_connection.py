"""
Quick connection check for the company Llama API.

This script checks:
1. Whether /models is reachable.
2. Whether /chat/completions responds to a very small JSON-only prompt.

It uses the same environment variables as main_llama.py:
- LLAMA_BASE_URL
- LLAMA_MODEL
- LLAMA_VERIFY_SSL
- LLAMA_USERNAME
- LLAMA_PASSWORD
- LLAMA_TIMEOUT, optional, default 60 seconds
"""

import os

import requests
import urllib3


def parse_bool(value: str | None, default: bool = True) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"true", "1", "yes", "y"}


def parse_timeout(value: str | None, default: int = 60) -> int:
    if value is None:
        return default
    try:
        return max(int(value), 10)
    except ValueError:
        return default


def main() -> None:
    base_url = os.getenv("LLAMA_BASE_URL")
    model = os.getenv("LLAMA_MODEL", "llama3.1:8b")
    username = os.getenv("LLAMA_USERNAME")
    password = os.getenv("LLAMA_PASSWORD")
    verify_ssl = parse_bool(os.getenv("LLAMA_VERIFY_SSL"), default=True)
    timeout = parse_timeout(os.getenv("LLAMA_TIMEOUT"), default=60)

    if not base_url:
        print("LLAMA_BASE_URL is not configured.")
        return

    if not verify_ssl:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    base_url = base_url.rstrip("/")
    auth = (username, password) if username and password else None

    print("Checking Llama API connection...")
    print("Base URL:", base_url)
    print("Model:", model)
    print("SSL verification:", verify_ssl)
    print("Timeout:", timeout)

    models_url = f"{base_url}/models"
    chat_url = f"{base_url}/chat/completions"

    try:
        print("\n1. Checking /models endpoint...")
        response = requests.get(models_url, auth=auth, verify=verify_ssl, timeout=timeout)
        print("Status code:", response.status_code)
        print("Response preview:", response.text[:500])
    except Exception as exc:
        print("/models check failed:", exc)

    try:
        print("\n2. Checking /chat/completions endpoint...")
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": "Return only this JSON object: {\"status\": \"ok\"}",
                }
            ],
            "temperature": 0.0,
        }
        response = requests.post(
            chat_url,
            auth=auth,
            json=payload,
            verify=verify_ssl,
            timeout=timeout,
        )
        print("Status code:", response.status_code)
        print("Response preview:", response.text[:1000])
    except Exception as exc:
        print("/chat/completions check failed:", exc)


if __name__ == "__main__":
    main()
