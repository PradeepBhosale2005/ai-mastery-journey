"""
Problem 11: Top K Frequent Elements

Given an integer array nums and an integer k, return the k most frequent elements.
The answer can be returned in any order.
"""

from collections import Counter
from typing import List


def top_k_frequent(nums: List[int], k: int) -> List[int]:
    counts = Counter(nums)
    return [number for number, _ in counts.most_common(k)]


if __name__ == "__main__":
    nums = [1, 1, 1, 2, 2, 3]
    k = 2
    print(top_k_frequent(nums, k))
