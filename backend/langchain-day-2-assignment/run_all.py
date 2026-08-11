"""Run all LangChain Day-2 assignment scripts."""

import subprocess
import sys
from pathlib import Path


SCRIPTS = [
    "assignment1_self_correcting_agent.py",
    "assignment2_smart_splitter.py",
    "assignment3_context_poisoning.py",
    "assignment4_fast_grounded_cache.py",
]


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    for script in SCRIPTS:
        print("=" * 80)
        print(f"Running {script}")
        print("=" * 80)
        subprocess.run([sys.executable, str(base_dir / script)], check=True)
        print()


if __name__ == "__main__":
    main()
