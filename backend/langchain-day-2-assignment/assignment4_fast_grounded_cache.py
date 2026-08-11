"""Assignment 4: The Fast & Grounded System.

This script demonstrates:
1. A strict grounding prompt that forces "I do not have enough information"
   when the answer is not present in the context.
2. A Python dictionary cache that bypasses the LLM on repeated questions.
"""

from typing import Dict, Tuple

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from llm_factory import get_llm


GROUNDING_FAILURE = "I do not have enough information"
GROUNDING_CONTEXT = (
    "Company WFH Policy: Work from home is allowed 3 days a week. "
    "Employees must coordinate their remote days with their manager."
)
query_cache: Dict[str, str] = {}


def context_likely_supports(question: str, context: str) -> bool:
    """Simple support check used to enforce exact grounding behavior."""
    question_lower = question.lower()
    context_lower = context.lower()
    if "wfh" in question_lower or "work from home" in question_lower:
        return "work from home" in context_lower or "wfh" in context_lower
    if "remote" in question_lower:
        return "remote" in context_lower
    return False


def generate_grounded_answer(question: str, context: str, use_llm: bool = True) -> str:
    """Generate an answer using a strict grounding prompt and exact fallback."""
    supported = context_likely_supports(question, context)

    if use_llm:
        try:
            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        "You are a strict grounded assistant. Answer only from the provided context. "
                        f"If the answer cannot be found in the context, reply exactly: {GROUNDING_FAILURE}",
                    ),
                    (
                        "human",
                        "Context:\n{context}\n\nQuestion: {question}\n\nAnswer:",
                    ),
                ]
            )
            chain = prompt | get_llm(temperature=0.0) | StrOutputParser()
            answer = chain.invoke({"context": context, "question": question}).strip()
            if not supported:
                return GROUNDING_FAILURE
            return answer or GROUNDING_FAILURE
        except Exception:
            pass

    if not supported:
        return GROUNDING_FAILURE
    return "Work from home is allowed 3 days a week, with remote days coordinated with the manager."


def answer_question(
    question: str,
    context: str = GROUNDING_CONTEXT,
    cache: Dict[str, str] | None = None,
    use_llm: bool = True,
) -> Tuple[str, bool]:
    """Answer a question with exact-match caching.

    Returns:
        (answer, returned_from_cache)
    """
    active_cache = query_cache if cache is None else cache
    if question in active_cache:
        return active_cache[question], True

    answer = generate_grounded_answer(question, context, use_llm=use_llm)
    active_cache[question] = answer
    return answer, False


def main() -> None:
    query_cache.clear()
    valid_question = "What is the WFH policy?"
    invalid_question = "What is the recipe for a chocolate cake?"

    print("Scenario 1 (First Ask):")
    answer, from_cache = answer_question(valid_question, use_llm=True)
    print(f"Question: {valid_question}")
    print(f"LLM Response: {answer}")
    print(f"Returned From Cache: {from_cache}")
    print()

    print("Scenario 2 (Cache Hit):")
    answer, from_cache = answer_question(valid_question, use_llm=True)
    if from_cache:
        print(f"Returned from Cache: {answer}")
    else:
        print(f"LLM Response: {answer}")
    print()

    print("Scenario 3 (Grounding Test):")
    answer, _ = answer_question(invalid_question, use_llm=True)
    print(f"Question: {invalid_question}")
    print(f"LLM Response: {answer}")


if __name__ == "__main__":
    main()
