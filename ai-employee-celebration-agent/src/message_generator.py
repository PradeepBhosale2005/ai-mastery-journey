from __future__ import annotations

import os
from typing import Any

import requests
from dotenv import load_dotenv

from src.models import CelebrationEvent


class CelebrationMessageGenerator:
    """Generate personalized celebration messages using a mock or OpenAI-compatible LLM."""

    def __init__(
        self,
        provider: str = "mock",
        base_url: str | None = None,
        model: str | None = None,
        username: str | None = None,
        password: str | None = None,
        verify_ssl: bool = False,
        timeout_seconds: int = 60,
    ) -> None:
        self.provider = provider.lower().strip()
        self.base_url = base_url
        self.model = model or "llama3.1:8b"
        self.username = username
        self.password = password
        self.verify_ssl = verify_ssl
        self.timeout_seconds = timeout_seconds

    @classmethod
    def from_env(cls) -> "CelebrationMessageGenerator":
        load_dotenv()
        verify_ssl = os.getenv("LLM_VERIFY_SSL", "false").strip().lower() == "true"
        timeout = int(os.getenv("LLM_TIMEOUT_SECONDS", "60"))
        return cls(
            provider=os.getenv("LLM_PROVIDER", "mock"),
            base_url=os.getenv("LLM_BASE_URL"),
            model=os.getenv("LLM_MODEL", "llama3.1:8b"),
            username=os.getenv("LLM_USERNAME"),
            password=os.getenv("LLM_PASSWORD"),
            verify_ssl=verify_ssl,
            timeout_seconds=timeout,
        )

    def generate(self, event: CelebrationEvent) -> str:
        if self.provider in {"company", "openai", "openai_compatible"} and self.base_url:
            try:
                return self._generate_with_openai_compatible_api(event)
            except Exception as exc:  # pragma: no cover - external API fallback path
                return self._mock_message(event, fallback_reason=str(exc))

        return self._mock_message(event)

    def _generate_with_openai_compatible_api(self, event: CelebrationEvent) -> str:
        endpoint = self.base_url.rstrip("/") + "/chat/completions"
        prompt = self._build_prompt(event)
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You write warm, inclusive, professional employee celebration messages. Return only the message text.",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7,
            "max_tokens": 160,
        }

        auth = (self.username, self.password) if self.username and self.password else None
        response = requests.post(
            endpoint,
            json=payload,
            auth=auth,
            timeout=self.timeout_seconds,
            verify=self.verify_ssl,
        )
        response.raise_for_status()
        data = response.json()
        message = data["choices"][0]["message"]["content"].strip()
        if not message:
            raise ValueError("LLM returned an empty message")
        return message

    def _build_prompt(self, event: CelebrationEvent) -> str:
        employee = event.employee
        if event.event_type == "birthday":
            occasion = "birthday"
            detail = "Do not mention age."
        else:
            occasion = f"{event.years}-year work anniversary"
            detail = "Mention appreciation for their contribution."

        return (
            f"Create a short celebration message for {employee.preferred_name}. "
            f"Occasion: {occasion}. Department: {employee.department}. Country: {employee.country}. "
            f"Tone: warm, professional, inclusive, and suitable for email or company social post. "
            f"{detail} Keep it under 70 words."
        )

    def _mock_message(self, event: CelebrationEvent, fallback_reason: str | None = None) -> str:
        employee = event.employee
        if event.event_type == "birthday":
            message = (
                f"Happy Birthday, {employee.preferred_name}! Wishing you a wonderful year ahead filled "
                f"with success, happiness, and exciting new opportunities. Thank you for being a valued "
                f"part of the {employee.department} team."
            )
        else:
            years = event.years or 1
            year_label = "year" if years == 1 else "years"
            message = (
                f"Congratulations, {employee.preferred_name}, on completing {years} {year_label} with us! "
                f"Your contribution to the {employee.department} team is truly appreciated. Wishing you "
                f"continued success and growth ahead."
            )

        if fallback_reason:
            return f"{message}"
        return message
