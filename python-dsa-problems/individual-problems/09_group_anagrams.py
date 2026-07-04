"""
Problem 9: Group Anagrams

Given an array of strings, group the anagrams together. The answer can be returned in any order.
"""

from collections import defaultdict
from typing import List


def group_anagrams(strings: List[str]) -> List[List[str]]:
    groups = defaultdict(list)

    for word in strings:
        key = tuple(sorted(word))
        groups[key].append(word)

    return list(groups.values())


if __name__ == "__main__":
    words = ["eat", "tea", "tan", "ate", "nat", "bat"]
    print(group_anagrams(words))
