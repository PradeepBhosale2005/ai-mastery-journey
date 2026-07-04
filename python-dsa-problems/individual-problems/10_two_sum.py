"""
Problem 10: Two Sum

Find indices of two numbers in an array that add up to a target.
"""

from typing import List


def two_sum(nums: List[int], target: int) -> List[int]:
    seen = {}

    for index, number in enumerate(nums):
        complement = target - number
        if complement in seen:
            return [seen[complement], index]
        seen[number] = index

    return []


if __name__ == "__main__":
    nums = [2, 7, 11, 15]
    target = 9
    print(two_sum(nums, target))
