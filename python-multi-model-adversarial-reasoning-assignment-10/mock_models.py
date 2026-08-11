"""Mock model clients for local testing without real company API calls."""

import json
import re


class MockModelClient:
    """A deterministic mock model that returns structured JSON."""

    def __init__(self, name: str) -> None:
        self.name = name

    def complete(self, prompt: str) -> str:
        """Return a mock JSON response based on the prompt type."""
        scenario = extract_scenario(prompt)

        if "Stress-test Model A" in prompt:
            response = (
                f"For the scenario '{scenario}', the proposal should be stress-tested for "
                "cost, feasibility, stakeholder impact, ethical concerns, security risks, "
                "edge cases, and implementation assumptions."
            )
            return json.dumps({"response": response})

        if "Revise, improve, or defend" in prompt:
            response = (
                f"For the scenario '{scenario}', the revised response strengthens the proposal "
                "by adding safeguards, implementation phases, monitoring, fallback plans, "
                "risk ownership, and measurable success criteria."
            )
            return json.dumps({"response": response})

        if "final evaluator" in prompt:
            evaluation = (
                f"For the scenario '{scenario}', the revised proposal is more robust because it "
                "addresses major risks, but remaining risks include execution complexity, "
                "resource limits, and ongoing governance needs."
            )
            return json.dumps({"evaluation": evaluation})

        response = (
            f"For the scenario '{scenario}', Model A proposes a practical solution with clear "
            "reasoning, expected benefits, implementation steps, and risk-aware decision points."
        )
        return json.dumps({"response": response})


def extract_scenario(prompt: str) -> str:
    """Extract a short scenario preview from a prompt."""
    match = re.search(
        r"Original user scenario or problem statement:\s*(.*?)\n\n",
        prompt,
        flags=re.DOTALL,
    )

    if not match:
        return "the provided problem"

    scenario = " ".join(match.group(1).split())
    return scenario[:90]
