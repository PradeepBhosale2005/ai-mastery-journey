"""
Command-line runner for the Article Analysis System.

Usage with company LLM API:
    python main.py sample_article.txt

Usage with a mock response for local validation:
    python main.py sample_article.txt --mock-response mock_valid_response.json
"""

import argparse
import sys
from pathlib import Path

from article_analyzer import (
    ArticleAnalysisError,
    analyze_article,
    analyze_article_from_raw_response,
    format_analysis_as_json,
)


def read_text_file(file_path: str) -> str:
    """Read and return text from a file."""
    return Path(file_path).read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze an article using a company-hosted LLM API.")
    parser.add_argument("article_file", help="Path to the article text file.")
    parser.add_argument(
        "--mock-response",
        help="Optional JSON file used to validate response parsing without calling the LLM API.",
    )
    args = parser.parse_args()

    try:
        article = read_text_file(args.article_file)

        if args.mock_response:
            raw_response = read_text_file(args.mock_response)
            analysis = analyze_article_from_raw_response(raw_response)
        else:
            analysis = analyze_article(article)

        print(format_analysis_as_json(analysis))
        return 0

    except FileNotFoundError as exc:
        print(f"File error: {exc}", file=sys.stderr)
        return 1
    except ArticleAnalysisError as exc:
        print(f"Article analysis failed: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Unexpected error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
