"""
Problem 4: Container With Most Water

Given an integer array height, find two lines that together with the x-axis form a
container that stores the maximum amount of water.
"""

from typing import List


def max_area(height: List[int]) -> int:
    left = 0
    right = len(height) - 1
    best_area = 0

    while left < right:
        width = right - left
        current_height = min(height[left], height[right])
        best_area = max(best_area, width * current_height)

        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return best_area


if __name__ == "__main__":
    height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    print(max_area(height))
