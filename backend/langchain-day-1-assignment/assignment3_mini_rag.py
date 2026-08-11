"""Assignment 3: Mini-RAG.

Loads made-up game rules from a text file, chunks them, embeds them, stores them
in an in-memory vector store, retrieves relevant context, and asks the LLM to
answer using only the retrieved rules.
"""

import argparse
import math
from pathlib import Path
from typing import List

from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter

from llm_factory import get_llm
from local_embeddings import HashEmbeddings


QUESTION = "How many points is the golden token worth?"
RULES_FILE = Path(__file__).with_name("game_rules.txt")


RAG_PROMPT = PromptTemplate.from_template(
    """
You are answering questions about a fictional board game.
Use only the retrieved rules below. If the answer is not present, say it is not in the rules.

Retrieved rules:
{context}

Question:
{question}

Answer clearly and briefly.
""".strip()
)


def _cosine_similarity(left: List[float], right: List[float]) -> float:
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return dot / (left_norm * right_norm)


def _fallback_similarity_search(
    documents: List[Document], embeddings: HashEmbeddings, query: str, k: int = 2
) -> List[Document]:
    """Fallback in-memory search when LangChain's vector store is unavailable."""
    query_vector = embeddings.embed_query(query)
    scored = []

    for document in documents:
        doc_vector = embeddings.embed_query(document.page_content)
        scored.append((_cosine_similarity(query_vector, doc_vector), document))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [document for _, document in scored[:k]]


def load_and_chunk_rules(file_path: Path) -> List[Document]:
    """Load rules with a LangChain Document Loader and split them into chunks."""
    loader = TextLoader(str(file_path), encoding="utf-8")
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=120, chunk_overlap=20)
    return splitter.split_documents(documents)


def retrieve_rules(question: str, file_path: Path = RULES_FILE) -> List[Document]:
    """Create embeddings, store chunks in memory, and retrieve relevant rules."""
    chunks = load_and_chunk_rules(file_path)
    embeddings = HashEmbeddings(dimensions=128)

    try:
        from langchain_core.vectorstores import InMemoryVectorStore

        vector_store = InMemoryVectorStore(embedding=embeddings)
        vector_store.add_documents(chunks)
        return vector_store.similarity_search(question, k=2)
    except Exception:
        return _fallback_similarity_search(chunks, embeddings, question, k=2)


def answer_question(question: str = QUESTION, file_path: Path = RULES_FILE) -> str:
    """Retrieve relevant rules and ask the LLM to answer the question."""
    retrieved_docs = retrieve_rules(question, file_path)
    context = "\n".join(document.page_content for document in retrieved_docs)

    chain = RAG_PROMPT | get_llm(temperature=0) | StrOutputParser()
    return chain.invoke({"context": context, "question": question}).strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a Mini-RAG query over game_rules.txt.")
    parser.add_argument("question", nargs="?", default=QUESTION)
    args = parser.parse_args()

    result = answer_question(args.question)
    print(result)


if __name__ == "__main__":
    main()
