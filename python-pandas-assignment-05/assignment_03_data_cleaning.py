"""
Assignment 3: Data Cleaning

1. Create a DataFrame with 3 columns and 5 rows. Introduce NaN values.
   Fill NaN values with the mean of the respective columns.
2. Create a DataFrame with 4 columns and 6 rows. Introduce NaN values.
   Drop rows with any NaN values.
"""

import numpy as np
import pandas as pd


def fill_nan_with_column_mean():
    rng = np.random.default_rng(42)
    df = pd.DataFrame(rng.integers(1, 101, size=(5, 3)).astype(float), columns=["A", "B", "C"])
    df.loc[1, "A"] = np.nan
    df.loc[3, "B"] = np.nan
    cleaned_df = df.fillna(df.mean(numeric_only=True))
    return df, cleaned_df


def drop_rows_with_nan():
    rng = np.random.default_rng(42)
    df = pd.DataFrame(rng.integers(1, 101, size=(6, 4)).astype(float), columns=["A", "B", "C", "D"])
    df.loc[1, "A"] = np.nan
    df.loc[4, "C"] = np.nan
    cleaned_df = df.dropna()
    return df, cleaned_df


if __name__ == "__main__":
    df, cleaned = fill_nan_with_column_mean()
    print("DataFrame with NaN values:")
    print(df)
    print("\nAfter filling NaN values with column mean:")
    print(cleaned)

    df, cleaned = drop_rows_with_nan()
    print("\nDataFrame with NaN values:")
    print(df)
    print("\nAfter dropping rows with NaN values:")
    print(cleaned)
