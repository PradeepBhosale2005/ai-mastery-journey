"""Shared LLM factory for LangChain Day-1 assignments.

Configuration is read from .env using python-dotenv. No API keys or passwords
are hardcoded. Supported providers:

- ollama: local Ollama runtime
- openai: OpenAI-compatible LangChain wrapper with standard API key
- gemini: Google Gemini LangChain wrapper
- company: company-hosted OpenAI-compatible chat endpoint using Basic Auth
"""

import os
from typing import Any, Dict, List, Optional, Tuple

from dotenv import load_dotenv
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.outputs import ChatGeneration, ChatResult


load_dotenv()


def _parse_bool(value: Optional[str], default: bool = True) -> bool:
    """Parse a boolean environment value."""
    if value is None or not value.strip():
        return default
    return value.strip().lower() in {"true", "1", "yes", "y"}


def _parse_int(value: Optional[str], default: int, minimum: int = 1) -> int:
    """Parse an integer environment value with a minimum."""
    if value is None or not value.strip():
        return default
    try:
        parsed = int(value)
    except ValueError:
        return default
    return max(parsed, minimum)


def _message_to_payload(message: BaseMessage) -> Dict[str, str]:
    """Convert a LangChain message to OpenAI-compatible message JSON."""
    if isinstance(message, SystemMessage):
        role = "system"
    elif isinstance(message, AIMessage):
        role = "assistant"
    elif isinstance(message, HumanMessage):
        role = "user"
    else:
        role = "user"

    return {"role": role, "content": str(message.content)}


def _extract_text_from_response(response_json: Dict[str, Any]) -> str:
    """Extract assistant text from common OpenAI-compatible response formats."""
    choices = response_json.get("choices")
    if isinstance(choices, list) and choices:
        first_choice = choices[0]
        if isinstance(first_choice, dict):
            message = first_choice.get("message")
            if isinstance(message, dict) and isinstance(message.get("content"), str):
                return message["content"]
            if isinstance(first_choice.get("text"), str):
                return first_choice["text"]

    for key in ["output_text", "content", "response"]:
        value = response_json.get(key)
        if isinstance(value, str):
            return value

    raise ValueError("Could not extract model text from company API response.")


class CompanyChatModel(BaseChatModel):
    """Small LangChain chat wrapper for a company-hosted OpenAI-compatible API."""

    base_url: str
    model: str
    username: Optional[str] = None
    password: Optional[str] = None
    verify_ssl: bool = True
    timeout: int = 180
    temperature: float = 0.2

    @property
    def _llm_type(self) -> str:
        """Return LangChain model type name."""
        return "company_openai_compatible_chat"

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Return non-secret identifying params."""
        return {
            "base_url": self.base_url,
            "model": self.model,
            "verify_ssl": self.verify_ssl,
            "timeout": self.timeout,
            "temperature": self.temperature,
        }

    def _chat_completions_url(self) -> str:
        """Return the chat completions URL."""
        base_url = self.base_url.rstrip("/")
        if base_url.endswith("/chat/completions"):
            return base_url
        return f"{base_url}/chat/completions"

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Any = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Call the company model and return a LangChain ChatResult."""
        import requests
        import urllib3

        if not self.verify_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": [_message_to_payload(message) for message in messages],
            "temperature": self.temperature,
        }
        if stop:
            payload["stop"] = stop

        auth: Optional[Tuple[str, str]] = None
        if self.username and self.password:
            auth = (self.username, self.password)

        response = requests.post(
            self._chat_completions_url(),
            headers={"Content-Type": "application/json"},
            json=payload,
            auth=auth,
            verify=self.verify_ssl,
            timeout=self.timeout,
        )
        response.raise_for_status()
        content = _extract_text_from_response(response.json())

        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=content))])


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

    if provider == "company":
        base_url = os.getenv("COMPANY_BASE_URL")
        model = os.getenv("COMPANY_MODEL")
        if not base_url:
            raise ValueError("COMPANY_BASE_URL is required when LLM_PROVIDER=company.")
        if not model:
            raise ValueError("COMPANY_MODEL is required when LLM_PROVIDER=company.")

        return CompanyChatModel(
            base_url=base_url,
            model=model,
            username=os.getenv("COMPANY_USERNAME"),
            password=os.getenv("COMPANY_PASSWORD"),
            verify_ssl=_parse_bool(os.getenv("COMPANY_VERIFY_SSL"), default=True),
            timeout=_parse_int(os.getenv("COMPANY_TIMEOUT"), default=180, minimum=30),
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
        f"Unsupported LLM_PROVIDER={provider!r}. Use ollama, company, openai, or gemini."
    )


def provider_name() -> str:
    """Return the configured provider name."""
    return os.getenv("LLM_PROVIDER", "ollama").strip().lower()
