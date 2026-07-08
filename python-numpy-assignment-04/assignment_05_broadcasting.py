"""
Assignment 5: Broadcasting

1. Create a NumPy array of shape (3, 3) filled with random integers.
   Add a 1D array of shape (3,) to each row using broadcasting.
2. Create a NumPy array of shape (4, 4) filled with random integers.
   Subtract a 1D array of shape (4,) from each column using broadcasting.
"""

import numpy as np


def add_array_to_each_row():
    """Add a 1D array to each row of a 3x3 matrix."""
    rng = np.random.default_rng(42)
    matrix = rng.integers(1, 11, size=(3, 3))
    row_values = np.array([10, 20, 30])
    result = matrix + row_values
    return matrix, row_values, result


def subtract_array_from_each_column():
    """Subtract a 1D array from each column of a 4x4 matrix."""
    rng = np.random.default_rng(42)
    matrix = rng.integers(1, 21, size=(4, 4))
    column_values = np.array([1, 2, 3, 4])
    result = matrix - column_values.reshape(4, 1)
    return matrix, column_values, result


if __name__ == "__main__":
    matrix, row_values, result = add_array_to_each_row()
    print("Original 3x3 matrix:")
    print(matrix)
    print("1D array:", row_values)
    print("Result after adding to each row:")
    print(result)

    matrix, column_values, result = subtract_array_from_each_column()
    print("\nOriginal 4x4 matrix:")
    print(matrix)
    print("1D array:", column_values)
    print("Result after subtracting from each column:")
    print(result)
