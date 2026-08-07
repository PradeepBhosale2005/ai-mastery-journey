"""JSONL logging for prompts, raw model outputs, and errors."""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


class InteractionLogger:
    """Write interaction events to a JSONL log file."""

    def __init__(self, log_path: str = "logs/interaction_log.jsonl") -> None:
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def log_event(self, event: Dict[str, Any]) -> None:
        """Append one event to the log file."""
        event_with_time = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **event,
        }

        with self.log_path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(event_with_time, ensure_ascii=False) + "\n")

    def log_prompt(self, turn: str, model_name: str, prompt: str) -> None:
        """Log a prompt sent to a model."""
        self.log_event(
            {
                "event_type": "prompt",
                "turn": turn,
                "model_name": model_name,
                "prompt": prompt,
            }
        )

    def log_raw_output(self, turn: str, model_name: str, raw_output: str) -> None:
        """Log raw model output."""
        self.log_event(
            {
                "event_type": "raw_output",
                "turn": turn,
                "model_name": model_name,
                "raw_output": raw_output,
            }
        )

    def log_error(self, turn: str, model_name: str, error_message: str) -> None:
        """Log an API or validation error."""
        self.log_event(
            {
                "event_type": "error",
                "turn": turn,
                "model_name": model_name,
                "error": error_message,
            }
        )
