"""Prompt construction logic for the multi-model interaction system."""


def build_model_a_initial_prompt(topic: str) -> str:
    """Prompt Model A for its initial position."""
    return f"""
You are Model A in a structured multi-model discussion.

Topic:
{topic}

Task:
Provide your initial position, explanation, or argument on the topic.

Return strictly valid JSON only, with this exact structure:
{{
  "response": "your relevant initial response about the topic"
}}
""".strip()


def build_model_b_critique_prompt(topic: str, model_a_response: str) -> str:
    """Prompt Model B to critique or expand on Model A."""
    return f"""
You are Model B in a structured multi-model discussion.

Original topic:
{topic}

Model A initial response:
{model_a_response}

Task:
Critique, question, or expand upon Model A's response while staying relevant to the original topic.

Return strictly valid JSON only, with this exact structure:
{{
  "response": "your critique or counter-response about the topic"
}}
""".strip()


def build_model_a_final_prompt(topic: str, model_a_response: str, model_b_response: str) -> str:
    """Prompt Model A for the final reply after Model B's critique."""
    return f"""
You are Model A in a structured multi-model discussion.

Original topic:
{topic}

Your initial response:
{model_a_response}

Model B critique or counter-response:
{model_b_response}

Task:
Write your final reply. Address Model B's points and stay relevant to the original topic.

Return strictly valid JSON only, with this exact structure:
{{
  "response": "your final reply about the topic"
}}
""".strip()


def build_synthesis_prompt(
    topic: str,
    model_a_initial_response: str,
    model_b_response: str,
    model_a_final_response: str,
) -> str:
    """Prompt one model to synthesize the discussion conclusion."""
    return f"""
You are the final synthesizer for a structured multi-model discussion.

Original topic:
{topic}

Model A initial response:
{model_a_initial_response}

Model B critique or counter-response:
{model_b_response}

Model A final reply:
{model_a_final_response}

Task:
Write a short synthesized conclusion that captures the main outcome of the discussion.

Return strictly valid JSON only, with this exact structure:
{{
  "conclusion": "short synthesized conclusion about the topic"
}}
""".strip()
