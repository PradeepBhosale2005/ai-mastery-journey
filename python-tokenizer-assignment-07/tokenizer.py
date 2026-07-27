"""
Tokenizer Assignment

This program takes one or more sentences, splits the text into tokens,
and dynamically maintains a vocabulary where each unique token receives
one unique numerical ID.
"""

import re
from typing import Dict, List, Tuple, Union


class SimpleTokenizer:
    """A simple word tokenizer that creates and maintains its own vocabulary."""

    def __init__(self) -> None:
        # word_to_id stores each unique token with its assigned numerical ID.
        self.word_to_id: Dict[str, int] = {}

        # id_to_word is useful if we want to convert IDs back to words.
        self.id_to_word: Dict[int, str] = {}

        # IDs start from 1 as shown in the assignment example.
        self.next_id = 1

    def tokenize(self, text: str) -> List[str]:
        """
        Convert text into lowercase word tokens.

        Punctuation is removed and only alphanumeric words are kept.
        Example:
        "This is a test." -> ["this", "is", "a", "test"]
        """
        return re.findall(r"[a-zA-Z0-9]+", text.lower())

    def add_token_to_vocabulary(self, token: str) -> int:
        """
        Add a token to the vocabulary if it is new.
        Reuse the existing ID if the token is already present.
        """
        if token not in self.word_to_id:
            self.word_to_id[token] = self.next_id
            self.id_to_word[self.next_id] = token
            self.next_id += 1

        return self.word_to_id[token]

    def encode(self, text: str) -> List[int]:
        """
        Tokenize the text, update the vocabulary, and return token IDs.
        """
        tokens = self.tokenize(text)
        token_ids = []

        for token in tokens:
            token_id = self.add_token_to_vocabulary(token)
            token_ids.append(token_id)

        return token_ids

    def process_text(self, text: str) -> Tuple[List[str], List[int], Dict[str, int]]:
        """
        Process text and return tokens, token IDs, and current vocabulary.
        """
        tokens = self.tokenize(text)
        token_ids = self.encode(text)
        return tokens, token_ids, self.get_vocabulary()

    def process_sentences(
        self, sentences: Union[str, List[str]]
    ) -> Tuple[List[str], List[int], Dict[str, int]]:
        """
        Process one sentence or multiple sentences.
        """
        if isinstance(sentences, list):
            text = " ".join(sentences)
        else:
            text = sentences

        return self.process_text(text)

    def get_vocabulary(self) -> Dict[str, int]:
        """Return a copy of the current vocabulary."""
        return dict(self.word_to_id)

    def decode(self, token_ids: List[int]) -> List[str]:
        """Convert a list of token IDs back to words."""
        return [self.id_to_word[token_id] for token_id in token_ids]


if __name__ == "__main__":
    tokenizer = SimpleTokenizer()

    sample_text = "This is a test. This test is simple."
    tokens, token_ids, vocabulary = tokenizer.process_text(sample_text)

    print("Input text:")
    print(sample_text)

    print("\nTokens:")
    print(tokens)

    print("\nToken IDs:")
    print(token_ids)

    print("\nVocabulary:")
    print(vocabulary)

    # Demonstrating dynamic vocabulary update with new text.
    new_text = "This tokenizer is useful."
    new_tokens, new_token_ids, updated_vocabulary = tokenizer.process_text(new_text)

    print("\nNew input text:")
    print(new_text)

    print("\nNew tokens:")
    print(new_tokens)

    print("\nNew token IDs:")
    print(new_token_ids)

    print("\nUpdated vocabulary:")
    print(updated_vocabulary)
