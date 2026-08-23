"""Run the document processing workflow with the bundled sample SRS."""

from __future__ import annotations

from document_workflow import load_srs_from_file, run_document_processing


def main() -> None:
    srs_text = load_srs_from_file("sample_srs.md")
    result = run_document_processing(
        srs_text=srs_text,
        source_name="sample_srs.md",
        human_review_comments="Sample run reviewed and approved for final report generation.",
    )

    print("LangGraph AI Document Processing Workflow")
    print("=========================================")
    print()
    print(result["final_report"])


if __name__ == "__main__":
    main()
