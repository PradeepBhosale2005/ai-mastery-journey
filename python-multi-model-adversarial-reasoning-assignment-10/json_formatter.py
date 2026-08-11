"""JSON formatting helpers for final application output."""

import json
from typing import Any, Dict


def format_success(result: Dict[str, Any]) -> str:
    """Return strictly valid formatted JSON for successful output."""
    return json.dumps(result, indent=2, ensure_ascii=False)


def format_error(error_message: str) -> str:
    """Return strictly valid formatted JSON for failures."""
    return json.dumps(
        {
            "status": "failed",
            "error": error_message,
        },
        indent=2,
        ensure_ascii=False,
    )


def format_failure(error_message: str) -> str:
    """Backward-compatible alias used by robust CLI runner."""
    return format_error(error_message)
