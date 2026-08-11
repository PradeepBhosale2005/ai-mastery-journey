"""Assignment 2: The Smart Splitter Proof.

Uses LangChain's RecursiveCharacterTextSplitter with:
- chunk_size = 200
- chunk_overlap = 50

The script proves the overlap by programmatically comparing consecutive chunks.
"""

from pathlib import Path
from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter


DOCUMENT_PATH = Path(__file__).with_name("long_document.txt")
CHUNK_SIZE = 200
CHUNK_OVERLAP = 50


def load_document() -> str:
    return DOCUMENT_PATH.read_text(encoding="utf-8")


def split_document(text: str) -> List[str]:
    """Split text with exact character-level recursive splitting."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[""],
    )
    return splitter.split_text(text)


def extract_overlap(previous_chunk: str, next_chunk: str, max_overlap: int = CHUNK_OVERLAP) -> str:
    """Return the largest suffix/prefix overlap between two consecutive chunks."""
    for length in range(max_overlap, 0, -1):
        candidate = previous_chunk[-length:]
        if next_chunk.startswith(candidate):
            return candidate
    return ""


def validate_exact_overlap(previous_chunk: str, next_chunk: str) -> bool:
    """Validate that the required 50-character overlap exists."""
    overlap = extract_overlap(previous_chunk, next_chunk)
    return len(overlap) == CHUNK_OVERLAP


def main() -> None:
    text = load_document()
    chunks = split_document(text)

    if len(chunks) < 2:
        raise RuntimeError("The document did not produce at least two chunks.")

    chunk_1 = chunks[0]
    chunk_2 = chunks[1]
    overlap = extract_overlap(chunk_1, chunk_2)

    print(f"Chunk Size Setting: {CHUNK_SIZE}")
    print(f"Chunk Overlap Setting: {CHUNK_OVERLAP}")
    print()
    print(f"Chunk 1: {chunk_1}")
    print()
    print(f"Chunk 2: {chunk_2}")
    print()
    print(f"Extracted Overlap: {overlap}")
    print(f"Extracted Overlap Length: {len(overlap)}")
    print(f"Overlap Validated: {validate_exact_overlap(chunk_1, chunk_2)}")

    print()
    print("All Chunk Pair Overlap Checks:")
    for index in range(len(chunks) - 1):
        pair_overlap = extract_overlap(chunks[index], chunks[index + 1])
        print(
            f"Chunk {index + 1} -> Chunk {index + 2}: "
            f"{len(pair_overlap)} characters overlapped"
        )


if __name__ == "__main__":
    main()
