"""Agent node logic for the LangGraph SRS document processing workflow.

Each function represents one agent or workflow step from the assignment diagram:
Input SRS -> Document Analyzer -> Requirement/Risk Agents -> Architecture/Test Agents
-> Merge Results -> Human Review HITL -> Final Report.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List

from state_schema import DocumentProcessingState


REQUIREMENT_KEYWORDS = ["must", "shall", "should", "will", "allow", "support", "validate", "route", "store"]
RISK_KEYWORDS = {
    "security": ["security", "access", "role", "employee data", "financial data", "protect"],
    "integration": ["integration", "erp", "payroll", "api", "external", "later phase"],
    "performance": ["seconds", "traffic", "uptime", "available", "availability"],
    "audit": ["audit", "logs", "timestamp", "approval trail"],
}


def _normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _split_sentences(text: str) -> List[str]:
    cleaned = text.replace("\n", " ")
    sentences = re.split(r"(?<=[.!?])\s+|\n+-\s+", cleaned)
    return [_normalize_whitespace(sentence.strip(" -")) for sentence in sentences if sentence.strip(" -")]


def _extract_title(text: str, source_name: str) -> str:
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("#"):
            return line.lstrip("#").strip()
    return source_name or "Software Requirement Document"


def _requirement_type(sentence: str) -> str:
    lowered = sentence.lower()
    if any(word in lowered for word in ["seconds", "uptime", "security", "available", "audit", "role-based"]):
        return "Non-Functional"
    return "Functional"


def _extract_requirements(text: str) -> List[Dict[str, str]]:
    requirements: List[Dict[str, str]] = []
    for sentence in _split_sentences(text):
        lowered = sentence.lower()
        if any(keyword in lowered for keyword in REQUIREMENT_KEYWORDS):
            requirements.append(
                {
                    "id": f"REQ-{len(requirements) + 1:03d}",
                    "type": _requirement_type(sentence),
                    "description": sentence,
                }
            )
    return requirements


def input_srs_node(state: DocumentProcessingState) -> DocumentProcessingState:
    """Validate that an SRS document was provided."""
    text = state.get("srs_text", "").strip()
    errors: List[str] = []
    if not text:
        errors.append("Input SRS is empty. Please provide a Software Requirement Document.")
    elif len(text.split()) < 30:
        errors.append("Input SRS is too short for meaningful multi-agent analysis.")

    return {
        "validation_errors": errors,
        "execution_trace": ["Input SRS: document received and basic validation completed."],
    }


def document_analyzer_node(state: DocumentProcessingState) -> DocumentProcessingState:
    """Analyze the document structure, title, summary, and statistics."""
    text = state.get("srs_text", "")
    title = _extract_title(text, state.get("source_name", "sample_srs.md"))
    sentences = _split_sentences(text)
    sections = [line.strip("# ") for line in text.splitlines() if line.strip().startswith("#")]
    summary = " ".join(sentences[:2]) if sentences else "No summary available."

    stats = {
        "word_count": len(text.split()),
        "sentence_count": len(sentences),
        "section_count": len(sections),
        "sections": sections,
    }

    return {
        "document_title": title,
        "document_summary": summary,
        "document_statistics": stats,
        "execution_trace": ["Document Analyzer: extracted title, summary, sections, and document statistics."],
    }


def requirement_agent_node(state: DocumentProcessingState) -> DocumentProcessingState:
    """Extract functional and non-functional requirements from the SRS."""
    requirements = _extract_requirements(state.get("srs_text", ""))
    gaps: List[str] = []

    text_lower = state.get("srs_text", "").lower()
    if "acceptance criteria" not in text_lower:
        gaps.append("Acceptance criteria are not explicitly defined.")
    if "priority" not in text_lower:
        gaps.append("Requirement priority is not specified.")
    if not requirements:
        gaps.append("No clear requirements were extracted from the SRS.")

    return {
        "extracted_requirements": requirements,
        "requirement_gaps": gaps,
        "execution_trace": [f"Requirement Agent: extracted {len(requirements)} requirements and {len(gaps)} gaps."],
    }


def risk_agent_node(state: DocumentProcessingState) -> DocumentProcessingState:
    """Identify delivery, security, integration, performance, and audit risks."""
    text_lower = state.get("srs_text", "").lower()
    risks: List[Dict[str, str]] = []

    for category, keywords in RISK_KEYWORDS.items():
        if any(keyword in text_lower for keyword in keywords):
            risks.append(
                {
                    "category": category.title(),
                    "severity": "Medium" if category != "security" else "High",
                    "description": f"The SRS contains {category}-related requirements that need validation and controls.",
                    "mitigation": f"Define measurable {category} acceptance criteria and review them during design.",
                }
            )

    if "later phase" in text_lower or "desirable" in text_lower:
        risks.append(
            {
                "category": "Scope",
                "severity": "Medium",
                "description": "Some features are deferred or optional, which can cause scope ambiguity.",
                "mitigation": "Separate MVP scope from future-phase enhancements before development starts.",
            }
        )

    if not risks:
        risks.append(
            {
                "category": "General",
                "severity": "Low",
                "description": "No major risk keywords were detected, but stakeholder review is still required.",
                "mitigation": "Conduct a walkthrough with product, architecture, QA, and operations teams.",
            }
        )

    return {
        "risk_findings": risks,
        "execution_trace": [f"Risk Agent: identified {len(risks)} risk areas."],
    }


def architecture_agent_node(state: DocumentProcessingState) -> DocumentProcessingState:
    """Create architecture recommendations based on extracted requirements."""
    requirements = state.get("extracted_requirements", [])
    combined_text = " ".join(req.get("description", "") for req in requirements).lower()

    recommendations = [
        "Use a layered architecture with UI, service, workflow, data, and notification components.",
        "Create an Expense Submission Service to validate amount, currency, receipt, category, and business purpose.",
        "Use a Workflow/Routing Service to apply approval policies and preserve an approval audit trail.",
    ]

    if "email" in combined_text or "notification" in combined_text:
        recommendations.append("Add a Notification Service for approval-completion emails.")
    if "role" in combined_text or "access" in combined_text or "protect" in combined_text:
        recommendations.append("Add role-based access control and centralized authorization checks.")
    if "audit" in combined_text or "timestamp" in combined_text:
        recommendations.append("Use immutable audit logging for every decision, approver, comment, and status change.")
    if "erp" in combined_text or "payroll" in combined_text or "integration" in combined_text:
        recommendations.append("Design integration adapters for ERP and payroll systems as separate future-ready modules.")

    return {
        "architecture_recommendations": recommendations,
        "execution_trace": [f"Architecture Agent: produced {len(recommendations)} architecture recommendations."],
    }


def test_case_agent_node(state: DocumentProcessingState) -> DocumentProcessingState:
    """Generate test cases using risk findings and expected document behavior."""
    risks = state.get("risk_findings", [])
    test_cases: List[Dict[str, str]] = [
        {
            "id": "TC-001",
            "title": "Submit valid expense claim",
            "scenario": "Employee submits amount, currency, date, category, business purpose, and receipt.",
            "expected_result": "System accepts the claim and starts approval routing.",
        },
        {
            "id": "TC-002",
            "title": "Reject invalid amount",
            "scenario": "Employee submits an expense amount less than or equal to zero.",
            "expected_result": "System rejects the claim with a validation message.",
        },
        {
            "id": "TC-003",
            "title": "Route high-value expense",
            "scenario": "Employee submits a high-value expense requiring finance review.",
            "expected_result": "System routes the claim to the finance department and records the decision trail.",
        },
    ]

    for risk in risks[:3]:
        test_cases.append(
            {
                "id": f"TC-{len(test_cases) + 1:03d}",
                "title": f"Validate {risk.get('category', 'risk')} control",
                "scenario": risk.get("description", "Validate identified risk area."),
                "expected_result": risk.get("mitigation", "Risk is controlled through review and acceptance criteria."),
            }
        )

    return {
        "test_cases": test_cases,
        "execution_trace": [f"Test Case Agent: generated {len(test_cases)} test cases."],
    }


def merge_results_node(state: DocumentProcessingState) -> DocumentProcessingState:
    """Merge all agent outputs into a structured insight package."""
    requirements = state.get("extracted_requirements", [])
    risks = state.get("risk_findings", [])
    architecture = state.get("architecture_recommendations", [])
    tests = state.get("test_cases", [])
    gaps = state.get("requirement_gaps", [])

    validation_errors = list(state.get("validation_errors", []))
    if not requirements:
        validation_errors.append("Merged validation failed: no requirements were found.")
    if not architecture:
        validation_errors.append("Merged validation failed: no architecture recommendations were produced.")
    if not tests:
        validation_errors.append("Merged validation failed: no test cases were produced.")

    merged = {
        "document_title": state.get("document_title", "Untitled SRS"),
        "summary": state.get("document_summary", ""),
        "statistics": state.get("document_statistics", {}),
        "requirements": requirements,
        "requirement_gaps": gaps,
        "risks": risks,
        "architecture_recommendations": architecture,
        "test_cases": tests,
        "validation_status": "Passed" if not validation_errors else "Needs Review",
    }

    return {
        "merged_results": merged,
        "validation_errors": validation_errors,
        "execution_trace": ["Merge Results: combined requirement, risk, architecture, and test-case outputs."],
    }


def human_review_hitl_node(state: DocumentProcessingState) -> DocumentProcessingState:
    """Simulate a Human-in-the-Loop review checkpoint."""
    comments = state.get("human_review_comments", "Reviewed by business analyst. Proceed with final report.")
    status = "APPROVED_BY_HUMAN_REVIEW"
    if state.get("validation_errors"):
        status = "APPROVED_WITH_REVIEW_NOTES"

    return {
        "human_review_status": status,
        "human_review_comments": comments,
        "execution_trace": [f"Human Review HITL: {status}."],
    }


def _format_bullets(items: List[str]) -> str:
    if not items:
        return "- None"
    return "\n".join(f"- {item}" for item in items)


def final_report_node(state: DocumentProcessingState) -> DocumentProcessingState:
    """Produce the final Markdown report."""
    merged = state.get("merged_results", {})
    requirements = merged.get("requirements", [])
    risks = merged.get("risks", [])
    architecture = merged.get("architecture_recommendations", [])
    tests = merged.get("test_cases", [])
    gaps = merged.get("requirement_gaps", [])
    errors = state.get("validation_errors", [])

    requirement_lines = [
        f"- {req.get('id')}: [{req.get('type')}] {req.get('description')}" for req in requirements
    ]
    risk_lines = [
        f"- {risk.get('category')} ({risk.get('severity')}): {risk.get('description')} Mitigation: {risk.get('mitigation')}"
        for risk in risks
    ]
    test_lines = [
        f"- {case.get('id')}: {case.get('title')} - Expected: {case.get('expected_result')}" for case in tests
    ]

    report = f"""# Final SRS Analysis Report

## Document
- Title: {merged.get('document_title', state.get('document_title', 'Untitled SRS'))}
- Source: {state.get('source_name', 'Not provided')}
- Validation Status: {merged.get('validation_status', 'Not evaluated')}

## Executive Summary
{merged.get('summary', 'No summary available.')}

## Document Statistics
- Word Count: {merged.get('statistics', {}).get('word_count', 0)}
- Sentence Count: {merged.get('statistics', {}).get('sentence_count', 0)}
- Section Count: {merged.get('statistics', {}).get('section_count', 0)}

## Requirement Agent Output
{_format_bullets(requirement_lines)}

## Requirement Gaps
{_format_bullets(gaps)}

## Risk Agent Output
{_format_bullets(risk_lines)}

## Architecture Agent Output
{_format_bullets(architecture)}

## Test Case Agent Output
{_format_bullets(test_lines)}

## Human Review HITL
- Status: {state.get('human_review_status', 'Not reviewed')}
- Comments: {state.get('human_review_comments', 'No comments')}

## Validation Notes
{_format_bullets(errors)}

## Execution Trace
{_format_bullets(state.get('execution_trace', []))}
"""

    return {
        "final_report": report,
        "execution_trace": ["Final Report: generated structured SRS analysis report."],
    }
