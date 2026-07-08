"""
Assignment 10: Masked Arrays

1. Create a masked array of shape (4, 4) with random integers and mask the elements greater than 10.
   Compute the sum of the unmasked elements.
2. Create a masked array of shape (3, 3) with random integers and mask the diagonal elements.
   Replace the masked elements with the mean of the unmasked elements.
"""

import numpy as np
import numpy.ma as ma


def mask_values_greater_than_ten():
    """Mask values greater than 10 and compute the sum of unmasked values."""
    rng = np.random.default_rng(42)
    array = rng.integers(1, 21, size=(4, 4))
    masked_array = ma.masked_greater(array, 10)
    unmasked_sum = masked_array.sum()
    return array, masked_array, unmasked_sum


def replace_diagonal_with_unmasked_mean():
    """Mask diagonal elements and replace them with the mean of unmasked values."""
    rng = np.random.default_rng(42)
    array = rng.integers(1, 21, size=(3, 3)).astype(float)
    diagonal_mask = np.eye(3, dtype=bool)
    masked_array = ma.array(array, mask=diagonal_mask)
    unmasked_mean = masked_array.mean()
    filled_array = masked_array.filled(unmasked_mean)
    return array, masked_array, unmasked_mean, filled_array


if __name__ == "__main__":
    array, masked_array, unmasked_sum = mask_values_greater_than_ten()
    print("Original 4x4 array:")
    print(array)
    print("Masked array with values greater than 10 masked:")
    print(masked_array)
    print("Sum of unmasked values:", unmasked_sum)

    array, masked_array, mean_value, filled_array = replace_diagonal_with_unmasked_mean()
    print("\nOriginal 3x3 array:")
    print(array)
    print("Masked diagonal array:")
    print(masked_array)
    print("Mean of unmasked values:", mean_value)
    print("Array after replacing masked values with mean:")
    print(filled_array)
