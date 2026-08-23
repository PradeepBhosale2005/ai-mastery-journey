"""Tests for LangGraph Assignment 02: AI Document Processing Workflow."""

from __future__ import annotations

import unittest

from agents import _extract_requirements
from document_workflow import build_document_processing_graph, load_srs_from_file, run_document_processing


class TestDocumentProcessingWorkflow(unittest.TestCase):
    def setUp(self) -> None:
        self.sample_text = load_srs_from_file("sample_srs.md")

    def test_graph_compiles(self) -> None:
        app = build_document_processing_graph()
        self.assertIsNotNone(app)

    def test_requirement_extraction_finds_multiple_requirements(self) -> None:
        requirements = _extract_requirements(self.sample_text)
        self.assertGreaterEqual(len(requirements), 8)
        self.assertTrue(any(req["type"] == "Functional" for req in requirements))
        self.assertTrue(any(req["type"] == "Non-Functional" for req in requirements))

    def test_workflow_generates_final_report(self) -> None:
        result = run_document_processing(self.sample_text, source_name="sample_srs.md")
        report = result["final_report"]
        self.assertIn("# Final SRS Analysis Report", report)
        self.assertIn("Requirement Agent Output", report)
        self.assertIn("Risk Agent Output", report)
        self.assertIn("Architecture Agent Output", report)
        self.assertIn("Test Case Agent Output", report)
        self.assertIn("Human Review HITL", report)

    def test_workflow_runs_all_assignment_nodes(self) -> None:
        result = run_document_processing(self.sample_text, source_name="sample_srs.md")
        trace = " ".join(result.get("execution_trace", []))
        self.assertIn("Input SRS", trace)
        self.assertIn("Document Analyzer", trace)
        self.assertIn("Requirement Agent", trace)
        self.assertIn("Risk Agent", trace)
        self.assertIn("Architecture Agent", trace)
        self.assertIn("Test Case Agent", trace)
        self.assertIn("Merge Results", trace)
        self.assertIn("Human Review HITL", trace)
        self.assertIn("Final Report", trace)

    def test_parallel_agent_outputs_are_merged(self) -> None:
        result = run_document_processing(self.sample_text, source_name="sample_srs.md")
        merged = result["merged_results"]
        self.assertGreaterEqual(len(merged["requirements"]), 8)
        self.assertGreaterEqual(len(merged["risks"]), 2)
        self.assertGreaterEqual(len(merged["architecture_recommendations"]), 3)
        self.assertGreaterEqual(len(merged["test_cases"]), 3)

    def test_human_review_status_is_present(self) -> None:
        result = run_document_processing(
            self.sample_text,
            source_name="sample_srs.md",
            human_review_comments="Human reviewer approved after checking gaps.",
        )
        self.assertIn("APPROVED", result["human_review_status"])
        self.assertEqual(result["human_review_comments"], "Human reviewer approved after checking gaps.")

    def test_empty_document_creates_validation_errors(self) -> None:
        result = run_document_processing("", source_name="empty.md")
        self.assertTrue(result.get("validation_errors"))
        self.assertIn("Needs Review", result["final_report"])


if __name__ == "__main__":
    unittest.main()
