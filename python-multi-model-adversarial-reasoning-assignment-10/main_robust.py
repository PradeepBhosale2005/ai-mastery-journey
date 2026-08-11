"""Robust CLI entry point for the Multi-Model Adversarial Reasoning System.

Use this runner when real company-hosted models add markdown, backticks, or
reasoning text around the JSON object. The final CLI output remains valid JSON.
"""

import argparse
import json
from pathlib import Path

from config_loader import load_local_config
from json_formatter import format_failure, format_success
from llm_client import LLMClient
from mock_models import MockModelClient
from orchestrator_robust import AdversarialReasoningSystem


def read_input_from_args(text_input: str, file_path: str) -> str:
    """Read scenario text from command-line text or a file."""
    if text_input and file_path:
        raise ValueError("Provide either direct text input or --file, not both.")

    if file_path:
        return Path(file_path).read_text(encoding="utf-8")

    if text_input:
        return text_input

    raise ValueError("Provide a scenario/problem statement or use --file.")


def build_system(use_mock: bool, log_path: str) -> AdversarialReasoningSystem:
    """Create the adversarial reasoning system with real or mock model clients."""
    if use_mock:
        model_a_client = MockModelClient("Model A")
        model_b_client = MockModelClient("Model B")
    else:
        model_a_client = LLMClient.from_environment("MODEL_A", name="Model A")
        model_b_client = LLMClient.from_environment("MODEL_B", name="Model B")

    return AdversarialReasoningSystem(model_a_client, model_b_client, log_path=log_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run adversarial reasoning between two LLM models.")
    parser.add_argument("input", nargs="?", help="Text-only scenario or problem statement")
    parser.add_argument("--file", help="Path to a text file containing the scenario/problem statement")
    parser.add_argument(
        "--config",
        default="local_model_config.txt",
        help="Optional local config file with model API credentials",
    )
    parser.add_argument("--mock", action="store_true", help="Run using mock model clients")
    parser.add_argument(
        "--log-path",
        default="logs/adversarial_robust_log.jsonl",
        help="Path for JSONL prompt/raw-output logs",
    )

    args = parser.parse_args()

    try:
        load_local_config(args.config)
        original_input = read_input_from_args(args.input, args.file)
        system = build_system(use_mock=args.mock, log_path=args.log_path)
        result = system.run(original_input)
        print(format_success(result))
    except Exception as exc:
        print(format_failure(str(exc)))


if __name__ == "__main__":
    main()
