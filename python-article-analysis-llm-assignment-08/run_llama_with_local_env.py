"""
Run the Llama article analyzer after loading local environment values from a file.

Default local configuration file name: local_llama_config.txt

The config file should contain KEY=VALUE lines, for example:
LLAMA_BASE_URL=https://example-server/v1
LLAMA_MODEL=llama3.1:8b
LLAMA_VERIFY_SSL=false
LLAMA_USERNAME=your-username
LLAMA_PASSWORD=your-password

Do not commit the real local config file to GitHub.
"""

import argparse
import os
from pathlib import Path

from main_llama_long_timeout import main as run_main


def load_local_config(config_path: str) -> None:
    """Load KEY=VALUE pairs from a local config file into environment variables."""
    path = Path(config_path)

    if not path.exists():
        print(f"Config file not found: {config_path}")
        print("Create the file locally and add your Llama settings.")
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        os.environ[key] = value


def main() -> None:
    parser = argparse.ArgumentParser(description="Load local Llama config and run analyzer.")
    parser.add_argument("article_file", help="Path to the article text file")
    parser.add_argument(
        "--config",
        default="local_llama_config.txt",
        help="Path to local config file containing Llama environment values",
    )
    parser.add_argument(
        "--output",
        default="llama_analysis_output.json",
        help="Path where JSON output should be saved",
    )

    args = parser.parse_args()

    load_local_config(args.config)

    import sys

    sys.argv = ["main_llama_long_timeout.py", args.article_file, "--output", args.output]
    run_main()


if __name__ == "__main__":
    main()
