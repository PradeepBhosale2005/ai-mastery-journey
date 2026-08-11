"""Assignment 1: The Messy Data Cleaner.

Uses PromptTemplate, an LLM wrapper, and StrOutputParser to extract a compact
sentiment and issue summary from a messy product review.
"""

import argparse

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from llm_factory import get_llm


SAMPLE_REVIEW = (
    "I bought this blender yesterday and it's absolutely terrible! "
    "The lid flew off while I was making a smoothie and my whole kitchen is "
    "covered in spinach. I want a refund!"
)


PROMPT = PromptTemplate.from_template(
    """
You are a customer support data extraction assistant.

Read the messy product review below and extract only the core information.

Messy review:
{messy_review}

Output only a comma-separated string in this exact format:
Sentiment: [Positive/Negative], Core Issue: [Brief summary of the problem]

Do not include bullet points, explanations, markdown, or any extra text.
""".strip()
)


def build_chain():
    """Build the LangChain chain for Assignment 1."""
    llm = get_llm(temperature=0)
    return PROMPT | llm | StrOutputParser()


def clean_review(messy_review: str) -> str:
    """Run the extraction chain for one messy review."""
    chain = build_chain()
    return chain.invoke({"messy_review": messy_review}).strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean a messy product review.")
    parser.add_argument(
        "review",
        nargs="?",
        default=SAMPLE_REVIEW,
        help="Messy product review text. Uses assignment sample when omitted.",
    )
    args = parser.parse_args()

    result = clean_review(args.review)
    print(result)


if __name__ == "__main__":
    main()
