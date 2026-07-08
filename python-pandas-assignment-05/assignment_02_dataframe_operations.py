"""
Assignment 2: DataFrame Operations

1. Create a DataFrame with 3 columns and 5 rows filled with random integers.
   Add a new column that is the product of the first two columns.
2. Create a DataFrame with 3 columns and 4 rows filled with random integers.
   Compute row-wise and column-wise sums.
"""

import numpy as np
import pandas as pd


def add_product_column():
    rng = np.random.default_rng(42)
    df = pd.DataFrame(rng.integers(1, 11, size=(5, 3)), columns=["A", "B", "C"])
    df["A_B_Product"] = df["A"] * df["B"]
    return df


def compute_row_column_sums():
    rng = np.random.default_rng(42)
    df = pd.DataFrame(rng.integers(1, 11, size=(4, 3)), columns=["A", "B", "C"])
    row_sums = df.sum(axis=1)
    column_sums = df.sum(axis=0)
    return df, row_sums, column_sums


if __name__ == "__main__":
    print("DataFrame with product column:")
    print(add_product_column())

    df, row_sums, column_sums = compute_row_column_sums()
    print("\nOriginal DataFrame:")
    print(df)
    print("\nRow-wise sums:")
    print(row_sums)
    print("\nColumn-wise sums:")
    print(column_sums)
