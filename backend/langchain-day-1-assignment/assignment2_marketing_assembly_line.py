"""Assignment 2: The Marketing Assembly Line.

Builds a two-step LangChain Expression Language sequence:
1. Generate a catchy 5-word English slogan from a product name.
2. Translate that slogan into French.
"""

import argparse

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

from llm_factory import get_llm


SLOGAN_PROMPT = PromptTemplate.from_template(
    """
Create one catchy English marketing slogan for this product:
{product_name}

Rules:
- Exactly 5 words.
- Output only the slogan.
- No quotes, markdown, or explanation.
""".strip()
)


TRANSLATION_PROMPT = PromptTemplate.from_template(
    """
Translate this English slogan into French.

English slogan:
{slogan}

Output only the French slogan.
""".strip()
)


def build_chain():
    """Build the two-step LCEL chain using the pipe operator."""
    llm = get_llm(temperature=0.4)
    output_parser = StrOutputParser()

    slogan_chain = SLOGAN_PROMPT | llm | output_parser
    translation_chain = TRANSLATION_PROMPT | llm | output_parser

    return slogan_chain | RunnableLambda(lambda slogan: {"slogan": slogan}) | translation_chain


def generate_french_slogan(product_name: str) -> str:
    """Generate a five-word English slogan and translate it to French."""
    chain = build_chain()
    return chain.invoke({"product_name": product_name}).strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate and translate a marketing slogan.")
    parser.add_argument("product_name", nargs="?", default="EcoBottle")
    args = parser.parse_args()

    result = generate_french_slogan(args.product_name)
    print(result)


if __name__ == "__main__":
    main()
