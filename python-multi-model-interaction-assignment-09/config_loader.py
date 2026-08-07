"""Load local KEY=VALUE configuration for model credentials."""

import os
from pathlib import Path


def load_local_config(config_path: str = "local_model_config.txt") -> None:
    """Load environment variables from a local config file if it exists."""
    path = Path(config_path)

    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        os.environ[key] = value
