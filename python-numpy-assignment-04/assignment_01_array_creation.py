"""
Assignment 1: Array Creation and Manipulation

1. Create a NumPy array of shape (5, 5) filled with random integers between 1 and 20.
   Replace all elements in the third column with 1.
2. Create a NumPy array of shape (4, 4) with values from 1 to 16.
   Replace the diagonal elements with 0.
"""

import numpy as np


def replace_third_column() -> np.ndarray:
    """Create a 5x5 random integer array and replace the third column with 1."""
    rng = np.random.default_rng(42)
    array = rng.integers(1, 21, size=(5, 5))
    array[:, 2] = 1
    return array


def replace_diagonal_with_zero() -> np.ndarray:
    """Create a 4x4 array from 1 to 16 and replace diagonal elements with 0."""
    array = np.arange(1, 17).reshape(4, 4)
    np.fill_diagonal(array, 0)
    return array


if __name__ == "__main__":
    print("Task 1: Third column replaced with 1")
    print(replace_third_column())

    print("\nTask 2: Diagonal elements replaced with 0")
    print(replace_diagonal_with_zero())
