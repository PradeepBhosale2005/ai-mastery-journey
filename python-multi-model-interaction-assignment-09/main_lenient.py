"""Lenient command-line entry point for the Multi-Model Interaction System.

Use this runner when the real company-hosted models return valid topic-related
answers, but the strict validator rejects phrasing that does not repeat the
exact topic words.
"""

import argparse
import json

from config_loader import load_local_config
from llm_client import LLMClient
from mock_models import MockModelClient
from orchestrator_lenient import MultiModelInteractionSystem


def build_system(use_mock: bool, log_path: str) -> MultiModelInteractionSystem:
    """Create the multi-model system with real clients or mock clients."""
    if use_mock:
        model_a_client = MockModelClient("Model A")
        model_b_client = MockModelClient("Model B")
    else:
        model_a_client = LLMClient.from_environment("MODEL_A", name="Model A")
        model_b_client = LLMClient.from_environment("MODEL_B", name="Model B")

    return MultiModelInteractionSystem(model_a_client, model_b_client, log_path=log_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a structured interaction between two LLM models.")
    parser.add_argument("topic", help="Topic for the two-model discussion")
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
        default="logs/interaction_log.jsonl",
        help="Path for JSONL prompt/raw-output logs",
    )

    args = parser.parse_args()

    try:
        load_local_config(args.config)
        system = build_system(use_mock=args.mock, log_path=args.log_path)
        result = system.run_interaction(args.topic)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as exc:
        error_result = {
            "status": "failed",
            "error": str(exc),
        }
        print(json.dumps(error_result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
