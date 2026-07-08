"""
Assignment 7: Advanced Array Manipulation

1. Create a NumPy array of shape (3, 3) with values from 1 to 9.
   Reshape the array to shape (1, 9) and then to shape (9, 1).
2. Create a NumPy array of shape (5, 5) filled with random integers.
   Flatten the array and then reshape it back to (5, 5).
"""

import numpy as np


def reshape_array_examples():
    """Reshape a 3x3 array into 1x9 and 9x1 arrays."""
    array = np.arange(1, 10).reshape(3, 3)
    reshaped_one_by_nine = array.reshape(1, 9)
    reshaped_nine_by_one = array.reshape(9, 1)
    return array, reshaped_one_by_nine, reshaped_nine_by_one


def flatten_and_reshape():
    """Flatten a 5x5 random array and reshape it back to 5x5."""
    rng = np.random.default_rng(42)
    array = rng.integers(1, 21, size=(5, 5))
    flattened = array.flatten()
    reshaped = flattened.reshape(5, 5)
    return array, flattened, reshaped


if __name__ == "__main__":
    original, one_by_nine, nine_by_one = reshape_array_examples()
    print("Original 3x3 array:")
    print(original)
    print("Reshaped to 1x9:")
    print(one_by_nine)
    print("Reshaped to 9x1:")
    print(nine_by_one)

    array, flattened, reshaped = flatten_and_reshape()
    print("\nOriginal 5x5 array:")
    print(array)
    print("Flattened array:")
    print(flattened)
    print("Reshaped back to 5x5:")
    print(reshaped)
