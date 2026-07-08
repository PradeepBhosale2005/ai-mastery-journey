"""
Assignment 6: Linear Algebra

1. Create a NumPy array of shape (3, 3) representing a matrix.
   Compute its determinant, inverse, and eigenvalues.
2. Create two NumPy arrays of shape (2, 3) and (3, 2).
   Perform matrix multiplication.
"""

import numpy as np


def matrix_properties():
    """Compute determinant, inverse, and eigenvalues of a 3x3 matrix."""
    matrix = np.array(
        [
            [4, 7, 2],
            [3, 6, 1],
            [2, 5, 3],
        ],
        dtype=float,
    )

    determinant = np.linalg.det(matrix)
    inverse = np.linalg.inv(matrix)
    eigenvalues = np.linalg.eigvals(matrix)

    return matrix, determinant, inverse, eigenvalues


def matrix_multiplication():
    """Multiply a 2x3 matrix with a 3x2 matrix."""
    matrix_one = np.array([[1, 2, 3], [4, 5, 6]])
    matrix_two = np.array([[7, 8], [9, 10], [11, 12]])
    product = np.matmul(matrix_one, matrix_two)
    return matrix_one, matrix_two, product


if __name__ == "__main__":
    matrix, determinant, inverse, eigenvalues = matrix_properties()
    print("3x3 matrix:")
    print(matrix)
    print("Determinant:", determinant)
    print("Inverse:")
    print(inverse)
    print("Eigenvalues:")
    print(eigenvalues)

    matrix_one, matrix_two, product = matrix_multiplication()
    print("\nMatrix one:")
    print(matrix_one)
    print("Matrix two:")
    print(matrix_two)
    print("Matrix multiplication result:")
    print(product)
