"""
Assignment 4: Statistical Operations

1. Create a NumPy array of shape (5, 5) filled with random integers.
   Compute mean, median, standard deviation, and variance.
2. Create a NumPy array of shape (3, 3) with values from 1 to 9.
   Normalize the array to have mean 0 and standard deviation 1.
"""

import numpy as np


def calculate_statistics():
    """Return a random array and its statistical values."""
    rng = np.random.default_rng(42)
    array = rng.integers(1, 101, size=(5, 5))

    return {
        "array": array,
        "mean": np.mean(array),
        "median": np.median(array),
        "standard_deviation": np.std(array),
        "variance": np.var(array),
    }


def normalize_array():
    """Normalize a 3x3 array so it has mean 0 and standard deviation 1."""
    array = np.arange(1, 10).reshape(3, 3).astype(float)
    normalized = (array - np.mean(array)) / np.std(array)
    return array, normalized


if __name__ == "__main__":
    stats = calculate_statistics()
    print("Random 5x5 array:")
    print(stats["array"])
    print("Mean:", stats["mean"])
    print("Median:", stats["median"])
    print("Standard deviation:", stats["standard_deviation"])
    print("Variance:", stats["variance"])

    original, normalized = normalize_array()
    print("\nOriginal 3x3 array:")
    print(original)
    print("\nNormalized array:")
    print(normalized)
    print("Normalized mean:", round(np.mean(normalized), 10))
    print("Normalized standard deviation:", round(np.std(normalized), 10))
