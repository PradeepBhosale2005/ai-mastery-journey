"""
Assignment 2: Array Indexing and Slicing

1. Create a NumPy array of shape (6, 6) with values from 1 to 36.
   Extract rows 3 to 5 and columns 2 to 4.
2. Create a NumPy array of shape (5, 5) with random integers.
   Extract the elements on the border.
"""

import numpy as np


def extract_subarray() -> tuple[np.ndarray, np.ndarray]:
    """Create a 6x6 array and get rows 3 to 5 and columns 2 to 4."""
    array = np.arange(1, 37).reshape(6, 6)
    sub_array = array[2:5, 1:4]
    return array, sub_array


def extract_border_elements() -> tuple[np.ndarray, np.ndarray]:
    """Create a 5x5 random array and collect border elements."""
    rng = np.random.default_rng(42)
    array = rng.integers(1, 21, size=(5, 5))

    border_values = []
    rows, columns = array.shape

    for row in range(rows):
        for column in range(columns):
            is_top = row == 0
            is_bottom = row == rows - 1
            is_left = column == 0
            is_right = column == columns - 1

            if is_top or is_bottom or is_left or is_right:
                border_values.append(array[row, column])

    return array, np.array(border_values)


if __name__ == "__main__":
    original_array, sub_array = extract_subarray()
    print("Original 6x6 array:")
    print(original_array)
    print("\nSub-array, rows 3 to 5 and columns 2 to 4:")
    print(sub_array)

    random_array, border = extract_border_elements()
    print("\nRandom 5x5 array:")
    print(random_array)
    print("\nBorder elements:")
    print(border)
