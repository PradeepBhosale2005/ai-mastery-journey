"""
Assignment 8: Fancy Indexing and Boolean Indexing

1. Create a NumPy array of shape (5, 5) filled with random integers.
   Use fancy indexing to extract the elements at the corners of the array.
2. Create a NumPy array of shape (4, 4) filled with random integers.
   Use boolean indexing to set all elements greater than 10 to 10.
"""

import numpy as np


def extract_corner_elements():
    """Extract the four corner elements of a 5x5 array using fancy indexing."""
    rng = np.random.default_rng(42)
    array = rng.integers(1, 21, size=(5, 5))
    corners = array[[0, 0, 4, 4], [0, 4, 0, 4]]
    return array, corners


def cap_values_greater_than_ten():
    """Set all values greater than 10 to 10 using boolean indexing."""
    rng = np.random.default_rng(42)
    array = rng.integers(1, 21, size=(4, 4))
    updated_array = array.copy()
    updated_array[updated_array > 10] = 10
    return array, updated_array


if __name__ == "__main__":
    array, corners = extract_corner_elements()
    print("5x5 array:")
    print(array)
    print("Corner elements:")
    print(corners)

    original, updated = cap_values_greater_than_ten()
    print("\nOriginal 4x4 array:")
    print(original)
    print("Array after setting values greater than 10 to 10:")
    print(updated)
