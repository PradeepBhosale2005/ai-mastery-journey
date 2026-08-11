"""Prompt construction logic for adversarial reasoning turns."""


def build_model_a_initial_prompt(user_input: str) -> str:
    """Build prompt for Model A's first proposal."""
    return f"""
You are Model A in a Multi-Model Adversarial Reasoning System.

Original user scenario or problem statement:
{user_input}

Task:
Generate a clear solution, proposal, or position with reasoning.
Your response must address the original scenario directly.

Return only valid JSON with exactly this field:
{{
  "response": "Model A's initial proposal and reasoning"
}}
""".strip()


def build_model_b_critique_prompt(user_input: str, model_a_initial: str) -> str:
    """Build prompt for Model B's adversarial critique."""
    return f"""
You are Model B in a Multi-Model Adversarial Reasoning System.

Original user scenario or problem statement:
{user_input}

Model A's initial proposal:
{model_a_initial}

Task:
Stress-test Model A's proposal. Identify weaknesses, risks, edge cases,
counterarguments, missing assumptions, and practical concerns.
Your critique must stay relevant to the original scenario.

Return only valid JSON with exactly this field:
{{
  "response": "Model B's critique, risks, edge cases, and counterarguments"
}}
""".strip()


def build_model_a_revision_prompt(user_input: str, model_a_initial: str, model_b_critique: str) -> str:
    """Build prompt for Model A's revised or defended response."""
    return f"""
You are Model A in a Multi-Model Adversarial Reasoning System.

Original user scenario or problem statement:
{user_input}

Your initial proposal:
{model_a_initial}

Model B's critique:
{model_b_critique}

Task:
Revise, improve, or defend your original proposal in response to Model B.
Address the strongest risks and edge cases raised by Model B.
Your response must stay relevant to the original scenario.

Return only valid JSON with exactly this field:
{{
  "response": "Model A's revised response or defended proposal"
}}
""".strip()


def build_final_evaluation_prompt(
    user_input: str,
    model_a_initial: str,
    model_b_critique: str,
    model_a_revised: str,
) -> str:
    """Build prompt for a concise final robustness evaluation."""
    return f"""
You are the final evaluator in a Multi-Model Adversarial Reasoning System.

Original user scenario or problem statement:
{user_input}

Model A's initial proposal:
{model_a_initial}

Model B's critique:
{model_b_critique}

Model A's revised response:
{model_a_revised}

Task:
Write a concise final evaluation summarizing:
1. How robust the revised proposal is.
2. Which risks were addressed.
3. Which important risks remain.

Return only valid JSON with exactly this field:
{{
  "evaluation": "concise final evaluation of robustness and remaining risks"
}}
""".strip()
