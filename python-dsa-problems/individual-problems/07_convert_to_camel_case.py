"""
Problem 7: Convert Sentence to CamelCase

Convert a given space-separated string into CamelCase.
"""


def convert_to_camel_case(sentence: str) -> str:
    words = sentence.split()
    return "".join(word[:1].upper() + word[1:].lower() for word in words)


if __name__ == "__main__":
    sentence = "hello world from python"
    print(convert_to_camel_case(sentence))
