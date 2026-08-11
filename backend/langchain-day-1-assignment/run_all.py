"""Run all LangChain Day-1 assignment tasks."""

from assignment1_messy_data_cleaner import SAMPLE_REVIEW, clean_review
from assignment2_marketing_assembly_line import generate_french_slogan
from assignment3_mini_rag import QUESTION, answer_question
from assignment4_token_receipt import run_with_approx_callback, run_with_openai_callback


def main() -> None:
    print("Assignment 1: Messy Data Cleaner")
    print(clean_review(SAMPLE_REVIEW))
    print("\n" + "=" * 60 + "\n")

    print("Assignment 2: Marketing Assembly Line")
    print(generate_french_slogan("EcoBottle"))
    print("\n" + "=" * 60 + "\n")

    print("Assignment 3: Mini-RAG")
    print(answer_question(QUESTION))
    print("\n" + "=" * 60 + "\n")

    print("Assignment 4: Callback and Token Receipt")
    if not run_with_openai_callback(SAMPLE_REVIEW):
        run_with_approx_callback(SAMPLE_REVIEW)


if __name__ == "__main__":
    main()
