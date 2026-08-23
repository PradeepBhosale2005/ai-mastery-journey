"""CLI runner for LangGraph Assignment 02: AI Document Processing Workflow."""

from __future__ import annotations

import argparse
from pathlib import Path

from document_workflow import load_srs_from_file, run_document_processing


DEFAULT_SAMPLE_FILE = "sample_srs.md"


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the LangGraph SRS document processing workflow.")
    parser.add_argument(
        "--file",
        default=DEFAULT_SAMPLE_FILE,
        help="Path to the SRS document. Defaults to sample_srs.md.",
    )
    parser.add_argument(
        "--review-comment",
        default="Reviewed by business analyst. Proceed with final report.",
        help="Human review/HITL comment to add before final report generation.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Optional file path to save the final report as Markdown.",
    )
    parser.add_argument(
        "--show-trace",
        action="store_true",
        help="Print workflow execution trace after the report.",
    )
    args = parser.parse_args()

    srs_text = load_srs_from_file(args.file)
    result = run_document_processing(
        srs_text=srs_text,
        source_name=args.file,
        human_review_comments=args.review_comment,
    )

    final_report = result["final_report"]
    print(final_report)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(final_report, encoding="utf-8")
        print(f"\nFinal report saved to: {output_path}")

    if args.show_trace:
        print("\nWorkflow Trace")
        print("--------------")
        for step in result.get("execution_trace", []):
            print(f"- {step}")


if __name__ == "__main__":
    main()
