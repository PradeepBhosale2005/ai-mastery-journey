"""
Problem 1: Contains Duplicate

Given an integer array, return True if any value appears at least twice in the array,
and return False if every element is distinct.
"""

from typing import List


def contains_duplicate(nums: List[int]) -> bool:
    return len(nums) != len(set(nums))


if __name__ == "__main__":
    nums = [1, 2, 3, 1]
    print(contains_duplicate(nums))
