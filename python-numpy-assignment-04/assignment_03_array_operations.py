"""
Assignment 3: Array Operations

This file shows element-wise operations and row/column sums using NumPy.
"""

import numpy as np


def element_wise_operations():
    rng = np.random.default_rng(42)
    array_one = rng.integers(1, 11, size=(3, 4))
    array_two = rng.integers(1, 11, size=(3, 4))

    addition = array_one + array_two
    subtraction = array_one - array_two
    multiplication = array_one * array_two
    division = array_one / array_two

    return array_one, array_two, addition, subtraction, multiplication, division


def row_column_sums():
    array = np.arange(1, 17).reshape(4, 4)
    row_sums = np.sum(array, axis=1)
    column_sums = np.sum(array, axis=0)
    return array, row_sums, column_sums


if __name__ == "__main__":
    a, b, add, sub, mul, div = element_wise_operations()
    print("Array one:")
    print(a)
    print("\nArray two:")
    print(b)
    print("\nAddition:")
    print(add)
    print("\nSubtraction:")
    print(sub)
    print("\nMultiplication:")
    print(mul)
    print("\nDivision:")
    print(div)

    array, row_sums, column_sums = row_column_sums()
    print("\n4x4 array:")
    print(array)
    print("Row-wise sums:", row_sums)
    print("Column-wise sums:", column_sums)
