"""
Assignment 9: Applying Functions

1. Create a DataFrame with 3 columns and 5 rows filled with random integers.
   Apply a function that doubles the values.
2. Create a DataFrame with 3 columns and 6 rows filled with random integers.
   Apply a lambda function to create a new column that is the sum of existing columns.
"""

import numpy as np
import pandas as pd


def double_dataframe_values():
    rng = np.random.default_rng(42)
    df = pd.DataFrame(rng.integers(1, 11, size=(5, 3)), columns=["A", "B", "C"])
    doubled = df.apply(lambda column: column * 2)
    return df, doubled


def add_row_sum_column():
    rng = np.random.default_rng(42)
    df = pd.DataFrame(rng.integers(1, 11, size=(6, 3)), columns=["A", "B", "C"])
    df["RowSum"] = df.apply(lambda row: row["A"] + row["B"] + row["C"], axis=1)
    return df


if __name__ == "__main__":
    df, doubled = double_dataframe_values()
    print("Original DataFrame:")
    print(df)
    print("\nDoubled DataFrame:")
    print(doubled)

    df = add_row_sum_column()
    print("\nDataFrame with RowSum column:")
    print(df)
