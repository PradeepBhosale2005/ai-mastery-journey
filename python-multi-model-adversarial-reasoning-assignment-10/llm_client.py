"""Retry-enabled OpenAI-compatible client for company-hosted LLM APIs."""

import os
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

import requests
import urllib3


class LLMClientError(Exception):
    """Raised when a model API call fails."""


@dataclass
class LLMClient:
    """Reusable client for one company-hosted model."""

    name: str
    base_url: str
    model: str
    username: Optional[str] = None
    password: Optional[str] = None
    verify_ssl: bool = True
    timeout: int = 180
    retries: int = 2
    retry_delay: int = 2

    @classmethod
    def from_environment(cls, prefix: str, name: str) -> "LLMClient":
        """Create a client from environment variables such as MODEL_A_BASE_URL."""
        base_url = os.getenv(f"{prefix}_BASE_URL")
        model = os.getenv(f"{prefix}_MODEL")
        username = os.getenv(f"{prefix}_USERNAME")
        password = os.getenv(f"{prefix}_PASSWORD")
        verify_ssl = parse_bool(os.getenv(f"{prefix}_VERIFY_SSL"), default=True)
        timeout = parse_int(os.getenv(f"{prefix}_TIMEOUT"), default=180, minimum=30)
        retries = parse_int(os.getenv(f"{prefix}_RETRIES"), default=2, minimum=0)
        retry_delay = parse_int(os.getenv(f"{prefix}_RETRY_DELAY"), default=2, minimum=0)

        if not base_url:
            raise LLMClientError(f"{prefix}_BASE_URL is not configured.")
        if not model:
            raise LLMClientError(f"{prefix}_MODEL is not configured.")

        return cls(
            name=name,
            base_url=base_url,
            model=model,
            username=username,
            password=password,
            verify_ssl=verify_ssl,
            timeout=timeout,
            retries=retries,
            retry_delay=retry_delay,
        )

    def chat_completions_url(self) -> str:
        """Return the OpenAI-compatible chat completions endpoint."""
        base_url = self.base_url.rstrip("/")

        if base_url.endswith("/chat/completions"):
            return base_url

        return f"{base_url}/chat/completions"

    def complete(self, prompt: str) -> str:
        """Send a prompt to the model and return raw response text with retries."""
        if not self.verify_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "Return only a valid JSON object. Do not include markdown or extra text.",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
        }

        auth: Optional[Tuple[str, str]] = None
        if self.username and self.password:
            auth = (self.username, self.password)

        last_error: Optional[Exception] = None
        total_attempts = self.retries + 1

        for attempt in range(1, total_attempts + 1):
            try:
                response = requests.post(
                    self.chat_completions_url(),
                    headers={"Content-Type": "application/json"},
                    json=payload,
                    auth=auth,
                    verify=self.verify_ssl,
                    timeout=self.timeout,
                )

                if response.status_code in {429, 500, 502, 503, 504} and attempt < total_attempts:
                    time.sleep(self.retry_delay)
                    continue

                response.raise_for_status()
                response_json = response.json()
                return extract_text_from_response(response_json)

            except requests.exceptions.Timeout as exc:
                last_error = exc
                if attempt < total_attempts:
                    time.sleep(self.retry_delay)
                    continue
                raise LLMClientError(
                    f"{self.name} request timed out after {self.timeout} seconds."
                ) from exc
            except requests.exceptions.ConnectionError as exc:
                last_error = exc
                if attempt < total_attempts:
                    time.sleep(self.retry_delay)
                    continue
                raise LLMClientError(f"{self.name} connection failed: {exc}") from exc
            except requests.exceptions.RequestException as exc:
                last_error = exc
                raise LLMClientError(f"{self.name} API request failed: {exc}") from exc
            except ValueError as exc:
                last_error = exc
                raise LLMClientError(f"{self.name} API response was not valid JSON.") from exc

        raise LLMClientError(f"{self.name} API request failed after retries: {last_error}")


def parse_bool(value: Optional[str], default: bool = True) -> bool:
    """Convert a string to a boolean."""
    if value is None:
        return default
    return value.strip().lower() in {"true", "1", "yes", "y"}


def parse_int(value: Optional[str], default: int, minimum: int) -> int:
    """Convert string to integer with a minimum allowed value."""
    if value is None:
        return default

    try:
        parsed = int(value)
    except ValueError:
        return default

    return max(parsed, minimum)


def extract_text_from_response(response_json: Dict[str, Any]) -> str:
    """Extract model text from common chat completion response formats."""
    if "choices" in response_json and response_json["choices"]:
        first_choice = response_json["choices"][0]

        if "message" in first_choice and "content" in first_choice["message"]:
            return first_choice["message"]["content"]

        if "text" in first_choice:
            return first_choice["text"]

    for key in ["output_text", "content", "response"]:
        if key in response_json and isinstance(response_json[key], str):
            return response_json[key]

    raise LLMClientError("Could not extract text from model response.")
