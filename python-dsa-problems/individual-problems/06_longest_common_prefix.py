"""
Problem 6: Longest Common Prefix

Given an array of strings, find the longest common prefix string shared among all of them.
"""

from typing import List


def longest_common_prefix(strings: List[str]) -> str:
    if not strings:
        return ""

    prefix = strings[0]

    for word in strings[1:]:
        while not word.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""

    return prefix


if __name__ == "__main__":
    words = ["flower", "flow", "flight"]
    print(longest_common_prefix(words))
