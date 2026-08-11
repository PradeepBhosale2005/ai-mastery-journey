"""Command-line entry point for the Multi-Model Adversarial Reasoning System."""

import argparse
from pathlib import Path

from config_loader import load_local_config
from json_formatter import format_error, format_success
from llm_client import LLMClient
from mock_models import MockModelClient
from orchestrator import AdversarialReasoningSystem


def read_original_input(args: argparse.Namespace) -> str:
    """Read the scenario from either command-line text or a file."""
    if args.file:
        return Path(args.file).read_text(encoding="utf-8")

    if args.scenario:
        return args.scenario

    raise ValueError("Provide a scenario as text or use --file scenario.txt")


def build_system(use_mock: bool, log_path: str) -> AdversarialReasoningSystem:
    """Create the adversarial reasoning system with real or mock clients."""
    if use_mock:
        model_a_client = MockModelClient("Model A")
        model_b_client = MockModelClient("Model B")
    else:
        model_a_client = LLMClient.from_environment("MODEL_A", name="Model A")
        model_b_client = LLMClient.from_environment("MODEL_B", name="Model B")

    return AdversarialReasoningSystem(model_a_client, model_b_client, log_path=log_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run adversarial reasoning between two LLM models.")
    parser.add_argument(
        "scenario",
        nargs="?",
        help="Text-only scenario or problem statement",
    )
    parser.add_argument(
        "--file",
        help="Optional path to a text file containing the scenario",
    )
    parser.add_argument(
        "--config",
        default="local_model_config.txt",
        help="Optional local config file with model API credentials",
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Run using mock model clients without calling real APIs",
    )
    parser.add_argument(
        "--log-path",
        default="logs/adversarial_log.jsonl",
        help="Path for JSONL prompt/raw-output logs",
    )

    args = parser.parse_args()

    try:
        load_local_config(args.config)
        original_input = read_original_input(args)
        system = build_system(use_mock=args.mock, log_path=args.log_path)
        result = system.run(original_input)
        print(format_success(result))
    except Exception as exc:
        print(format_error(str(exc)))


if __name__ == "__main__":
    main()
