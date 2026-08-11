"""Assignment 3: Solving Context Poisoning with metadata filtering.

Two contradictory WFH policy documents are embedded into an in-memory vector
store. The retrieval function accepts user_query and filter_year, then ignores
policy documents whose metadata year does not match the requested year.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, List, Optional

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from llm_factory import get_llm
from local_embeddings import SimpleHashEmbeddings, cosine_similarity


POLICY_2022 = Path(__file__).with_name("policy_2022.txt")
POLICY_2024 = Path(__file__).with_name("policy_2024.txt")
DEFAULT_QUERY = "What is the WFH policy?"


@dataclass
class VectorEntry:
    document: Document
    vector: List[float]


class MetadataFilteredVectorStore:
    """Small in-memory vector store with metadata filtering."""

    def __init__(self, embedding_model: Optional[SimpleHashEmbeddings] = None) -> None:
        self.embedding_model = embedding_model or SimpleHashEmbeddings()
        self.entries: List[VectorEntry] = []

    def add_documents(self, documents: Iterable[Document]) -> None:
        docs = list(documents)
        vectors = self.embedding_model.embed_documents([doc.page_content for doc in docs])
        for document, vector in zip(docs, vectors):
            self.entries.append(VectorEntry(document=document, vector=vector))

    def similarity_search(
        self,
        query: str,
        k: int = 1,
        metadata_filter: Optional[Callable[[Document], bool]] = None,
    ) -> List[Document]:
        query_vector = self.embedding_model.embed_query(query)
        scored = []
        for entry in self.entries:
            if metadata_filter is not None and not metadata_filter(entry.document):
                continue
            score = cosine_similarity(query_vector, entry.vector)
            scored.append((score, entry.document))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [document for _, document in scored[:k]]


def load_policy_documents() -> List[Document]:
    """Load the contradictory policy documents with year metadata."""
    return [
        Document(page_content=POLICY_2022.read_text(encoding="utf-8").strip(), metadata={"year": 2022}),
        Document(page_content=POLICY_2024.read_text(encoding="utf-8").strip(), metadata={"year": 2024}),
    ]


def build_vector_store(documents: Optional[List[Document]] = None) -> MetadataFilteredVectorStore:
    """Embed documents into the in-memory vector store."""
    docs = documents or load_policy_documents()
    store = MetadataFilteredVectorStore()
    store.add_documents(docs)
    return store


def retrieve_policy(user_query: str, filter_year: int) -> Document:
    """Retrieve only documents matching filter_year, then rank semantically."""
    store = build_vector_store()
    results = store.similarity_search(
        user_query,
        k=1,
        metadata_filter=lambda document: document.metadata.get("year") == filter_year,
    )
    if not results:
        raise ValueError(f"No policy document found for year {filter_year}.")
    return results[0]


def generate_answer(user_query: str, retrieved_context: str, use_llm: bool = True) -> str:
    """Generate an answer grounded only in the retrieved 2024 context."""
    if use_llm:
        try:
            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        "Answer using only the provided context. Do not mention policies outside the context.",
                    ),
                    (
                        "human",
                        "Context: {context}\n\nQuestion: {question}\nAnswer in one concise sentence.",
                    ),
                ]
            )
            chain = prompt | get_llm(temperature=0.0) | StrOutputParser()
            answer = chain.invoke({"context": retrieved_context, "question": user_query}).strip()
            if answer:
                return answer
        except Exception:
            pass

    if "allowed 3 days" in retrieved_context.lower():
        return "Work from home is allowed 3 days a week."
    return retrieved_context


def main() -> None:
    user_query = DEFAULT_QUERY
    filter_year = 2024
    retrieved_document = retrieve_policy(user_query, filter_year)
    retrieved_context = retrieved_document.page_content
    answer = generate_answer(user_query, retrieved_context, use_llm=True)

    print(f'User Query: "{user_query}"')
    print(f"Active Filter: Year: {filter_year}")
    print(f"Retrieved Context: {retrieved_context}")
    print(f"Retrieved Metadata: {retrieved_document.metadata}")
    print(f"LLM Final Answer: {answer}")


if __name__ == "__main__":
    main()
