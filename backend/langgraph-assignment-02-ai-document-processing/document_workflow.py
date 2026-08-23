"""LangGraph workflow for AI Document Processing of an SRS."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from langgraph.graph import END, START, StateGraph

from agents import (
    architecture_agent_node,
    document_analyzer_node,
    final_report_node,
    human_review_hitl_node,
    input_srs_node,
    merge_results_node,
    requirement_agent_node,
    risk_agent_node,
    test_case_agent_node,
)
from state_schema import DocumentProcessingState


def build_document_processing_graph():
    """Build and compile the LangGraph workflow from the assignment diagram."""
    graph = StateGraph(DocumentProcessingState)

    graph.add_node("input_srs", input_srs_node)
    graph.add_node("document_analyzer", document_analyzer_node)
    graph.add_node("requirement_agent", requirement_agent_node)
    graph.add_node("risk_agent", risk_agent_node)
    graph.add_node("architecture_agent", architecture_agent_node)
    graph.add_node("test_case_agent", test_case_agent_node)
    graph.add_node("merge_results", merge_results_node)
    graph.add_node("human_review_hitl", human_review_hitl_node)
    graph.add_node("final_report", final_report_node)

    graph.add_edge(START, "input_srs")
    graph.add_edge("input_srs", "document_analyzer")
    graph.add_edge("document_analyzer", "requirement_agent")
    graph.add_edge("document_analyzer", "risk_agent")
    graph.add_edge("requirement_agent", "architecture_agent")
    graph.add_edge("risk_agent", "test_case_agent")
    graph.add_edge(["architecture_agent", "test_case_agent"], "merge_results")
    graph.add_edge("merge_results", "human_review_hitl")
    graph.add_edge("human_review_hitl", "final_report")
    graph.add_edge("final_report", END)

    return graph.compile()


def run_document_processing(
    srs_text: str,
    source_name: str = "sample_srs.md",
    human_review_comments: Optional[str] = None,
) -> DocumentProcessingState:
    """Run the document-processing workflow and return the final state."""
    app = build_document_processing_graph()
    initial_state: DocumentProcessingState = {
        "srs_text": srs_text,
        "source_name": source_name,
        "human_review_comments": human_review_comments
        or "Reviewed by business analyst. Proceed with final report.",
        "execution_trace": [],
    }
    return app.invoke(initial_state)


def load_srs_from_file(path: str) -> str:
    """Load an SRS document from a text or Markdown file."""
    return Path(path).read_text(encoding="utf-8")
