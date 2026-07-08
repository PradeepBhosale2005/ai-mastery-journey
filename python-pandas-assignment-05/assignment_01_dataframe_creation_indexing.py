"""
Assignment 1: DataFrame Creation and Indexing

1. Create a Pandas DataFrame with 4 columns and 6 rows filled with random integers.
   Set the index to be the first column.
2. Create a Pandas DataFrame with columns A, B, C and index X, Y, Z.
   Fill it with random integers and access the element at row Y and column B.
"""

import numpy as np
import pandas as pd


def dataframe_with_first_column_as_index():
    rng = np.random.default_rng(42)
    data = rng.integers(1, 101, size=(6, 4))
    df = pd.DataFrame(data, columns=["ID", "Marks1", "Marks2", "Marks3"])
    df = df.set_index("ID")
    return df


def access_element_by_label():
    rng = np.random.default_rng(42)
    data = rng.integers(1, 101, size=(3, 3))
    df = pd.DataFrame(data, columns=["A", "B", "C"], index=["X", "Y", "Z"])
    value = df.loc["Y", "B"]
    return df, value


if __name__ == "__main__":
    print("DataFrame with first column as index:")
    print(dataframe_with_first_column_as_index())

    df, value = access_element_by_label()
    print("\nDataFrame with labels:")
    print(df)
    print("\nValue at row Y and column B:", value)
