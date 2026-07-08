"""
Assignment 7: MultiIndex DataFrame

1. Create a DataFrame with a MultiIndex and perform basic indexing and slicing.
2. Create a DataFrame with MultiIndex using Category and SubCategory and compute sums.
"""

import numpy as np
import pandas as pd


def basic_multiindex_operations():
    arrays = [["A", "A", "B", "B"], ["One", "Two", "One", "Two"]]
    index = pd.MultiIndex.from_arrays(arrays, names=["Group", "Type"])
    df = pd.DataFrame({"Value1": [10, 20, 30, 40], "Value2": [5, 15, 25, 35]}, index=index)
    group_a = df.loc["A"]
    group_b_type_two = df.loc[("B", "Two")]
    return df, group_a, group_b_type_two


def category_subcategory_sum():
    rng = np.random.default_rng(42)
    index = pd.MultiIndex.from_product(
        [["Electronics", "Furniture"], ["Small", "Large"]],
        names=["Category", "SubCategory"],
    )
    df = pd.DataFrame({"Value": rng.integers(100, 501, size=len(index))}, index=index)
    summed = df.groupby(level=["Category", "SubCategory"]).sum()
    return df, summed


if __name__ == "__main__":
    df, group_a, group_b_type_two = basic_multiindex_operations()
    print("MultiIndex DataFrame:")
    print(df)
    print("\nIndexing Group A:")
    print(group_a)
    print("\nIndexing Group B, Type Two:")
    print(group_b_type_two)

    df, summed = category_subcategory_sum()
    print("\nCategory and SubCategory DataFrame:")
    print(df)
    print("\nSum by Category and SubCategory:")
    print(summed)
