"""State schema for the LangGraph SRS document processing workflow."""

from __future__ import annotations

import operator
from typing import Annotated, Any, Dict, List, TypedDict


class DocumentProcessingState(TypedDict, total=False):
    """Shared graph state passed across all LangGraph nodes."""

    srs_text: str
    source_name: str
    document_title: str
    document_summary: str
    document_statistics: Dict[str, Any]
    extracted_requirements: List[Dict[str, str]]
    requirement_gaps: List[str]
    risk_findings: List[Dict[str, str]]
    architecture_recommendations: List[str]
    test_cases: List[Dict[str, str]]
    merged_results: Dict[str, Any]
    human_review_status: str
    human_review_comments: str
    final_report: str
    validation_errors: List[str]
    execution_trace: Annotated[List[str], operator.add]
