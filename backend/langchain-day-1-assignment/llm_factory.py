"""Shared LLM factory for LangChain Day-1 assignments.

Configuration is read from .env using python-dotenv. No API keys are hardcoded.
Default provider is local Ollama because the assignment notes that corporate
security may block external SaaS API keys.
"""

import os
from typing import Any

from dotenv import load_dotenv


load_dotenv()


def get_llm(temperature: float = 0.2) -> Any:
    """Create a LangChain chat model based on LLM_PROVIDER in .env."""
    provider = os.getenv("LLM_PROVIDER", "ollama").strip().lower()

    if provider == "ollama":
        from langchain_ollama import ChatOllama

        return ChatOllama(
            model=os.getenv("OLLAMA_MODEL", "llama3.1:8b"),
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            temperature=temperature,
        )

    if provider == "openai":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=temperature,
        )

    if provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(
            model=os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
            temperature=temperature,
        )

    raise ValueError(
        f"Unsupported LLM_PROVIDER={provider!r}. Use ollama, openai, or gemini."
    )


def provider_name() -> str:
    """Return the configured provider name."""
    return os.getenv("LLM_PROVIDER", "ollama").strip().lower()
