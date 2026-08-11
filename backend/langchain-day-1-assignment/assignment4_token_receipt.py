"""Assignment 4: The Watchful Eye.

Runs Assignment 1 with a LangChain callback/token counter and prints a clean
receipt showing total tokens, prompt tokens, completion tokens, and total cost.
"""

import argparse
import os
import re
from typing import Any, Iterable

from langchain_core.callbacks import BaseCallbackHandler

from assignment1_messy_data_cleaner import SAMPLE_REVIEW, build_chain
from llm_factory import provider_name


class ApproxTokenCallbackHandler(BaseCallbackHandler):
    """Simple callback handler that estimates tokens for non-OpenAI providers."""

    def __init__(self, cost_per_1000_tokens: float = 0.0) -> None:
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.cost_per_1000_tokens = cost_per_1000_tokens

    @staticmethod
    def estimate_tokens(text: str) -> int:
        """Estimate tokens using words and punctuation.

        This is intentionally simple and works for local Ollama demos where the
        API does not return billing/token metadata through LangChain callbacks.
        """
        if not text:
            return 0
        return len(re.findall(r"\w+|[^\w\s]", text))

    def on_llm_start(
        self,
        serialized: dict[str, Any],
        prompts: list[str],
        **kwargs: Any,
    ) -> None:
        self.prompt_tokens += sum(self.estimate_tokens(prompt) for prompt in prompts)

    def on_chat_model_start(
        self,
        serialized: dict[str, Any],
        messages: list[list[Any]],
        **kwargs: Any,
    ) -> None:
        for message_group in messages:
            for message in message_group:
                content = getattr(message, "content", "")
                self.prompt_tokens += self.estimate_tokens(str(content))

    def on_llm_end(self, response: Any, **kwargs: Any) -> None:
        for generation in self._iter_generations(response):
            text = getattr(generation, "text", "")
            message = getattr(generation, "message", None)
            if message is not None:
                text = getattr(message, "content", text)
            self.completion_tokens += self.estimate_tokens(str(text))

    @staticmethod
    def _iter_generations(response: Any) -> Iterable[Any]:
        generations = getattr(response, "generations", [])
        for generation_list in generations:
            for generation in generation_list:
                yield generation

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens

    @property
    def total_cost(self) -> float:
        return (self.total_tokens / 1000.0) * self.cost_per_1000_tokens


def _float_from_env(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, str(default)))
    except ValueError:
        return default


def print_receipt(
    result: str,
    total_tokens: int,
    prompt_tokens: int,
    completion_tokens: int,
    total_cost: float,
) -> None:
    """Print result and token receipt in a clean format."""
    print("Assignment 1 Output:")
    print(result)
    print()
    print("Token Usage Receipt")
    print("-------------------")
    print(f"Total Tokens Used: {total_tokens}")
    print(f"Prompt Tokens: {prompt_tokens}")
    print(f"Completion Tokens: {completion_tokens}")
    print(f"Total Cost: ${total_cost:.6f}")


def run_with_openai_callback(review: str) -> bool:
    """Use LangChain's OpenAI callback when the provider is OpenAI."""
    if provider_name() != "openai":
        return False

    try:
        from langchain_community.callbacks import get_openai_callback
    except Exception:
        return False

    chain = build_chain()
    with get_openai_callback() as callback:
        result = chain.invoke({"messy_review": review}).strip()

    print_receipt(
        result=result,
        total_tokens=callback.total_tokens,
        prompt_tokens=callback.prompt_tokens,
        completion_tokens=callback.completion_tokens,
        total_cost=callback.total_cost,
    )
    return True


def run_with_approx_callback(review: str) -> None:
    """Use a custom LangChain callback for Ollama/Gemini/local providers."""
    cost_per_1000 = _float_from_env("COST_PER_1000_TOKENS", default=0.0)
    token_counter = ApproxTokenCallbackHandler(cost_per_1000_tokens=cost_per_1000)

    chain = build_chain()
    result = chain.invoke(
        {"messy_review": review},
        config={"callbacks": [token_counter]},
    ).strip()

    print_receipt(
        result=result,
        total_tokens=token_counter.total_tokens,
        prompt_tokens=token_counter.prompt_tokens,
        completion_tokens=token_counter.completion_tokens,
        total_cost=token_counter.total_cost,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Assignment 1 with token/cost logging.")
    parser.add_argument("review", nargs="?", default=SAMPLE_REVIEW)
    args = parser.parse_args()

    if not run_with_openai_callback(args.review):
        run_with_approx_callback(args.review)


if __name__ == "__main__":
    main()
