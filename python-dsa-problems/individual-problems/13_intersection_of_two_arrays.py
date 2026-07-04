"""
Problem 13: Intersection of Two Arrays

Find the common elements between two arrays.
"""

from typing import List


def intersection(nums1: List[int], nums2: List[int]) -> List[int]:
    return sorted(list(set(nums1).intersection(set(nums2))))


if __name__ == "__main__":
    nums1 = [1, 2, 2, 1]
    nums2 = [2, 2]
    print(intersection(nums1, nums2))
