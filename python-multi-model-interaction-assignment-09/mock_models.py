"""Mock model clients for local testing without real company APIs."""

import json


class MockModelClient:
    """Mock model that returns structured JSON responses."""

    def __init__(self, name: str) -> None:
        self.name = name

    def complete(self, prompt: str) -> str:
        """Return deterministic mock JSON based on the model name and prompt."""
        topic = extract_topic_from_prompt(prompt)

        if "synthesized conclusion" in prompt.lower() or "final synthesizer" in prompt.lower():
            return json.dumps(
                {
                    "conclusion": f"The discussion shows that {topic} requires balanced analysis, practical safeguards, and thoughtful implementation."
                }
            )

        if self.name.lower() == "model a":
            if "final reply" in prompt.lower():
                response = f"Model A final reply: {topic} remains important, and Model B's critique strengthens the need for careful evaluation."
            else:
                response = f"Model A initial response: {topic} is significant because it can create benefits when applied responsibly."
        else:
            response = f"Model B critique: {topic} also has risks and limitations, so Model A's position should include stronger safeguards."

        return json.dumps({"response": response})


def extract_topic_from_prompt(prompt: str) -> str:
    """Extract a topic line from the prompt for mock responses."""
    lines = [line.strip() for line in prompt.splitlines()]

    for index, line in enumerate(lines):
        if line.lower() in {"topic:", "original topic:"} and index + 1 < len(lines):
            return lines[index + 1]

    return "the provided topic"
