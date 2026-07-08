"""
Assignment 8: Pivot Tables

1. Create a DataFrame with Date, Category, and Value. Create a pivot table to
   compute sum of Value for each Category by Date.
2. Create a DataFrame with Year, Quarter, and Revenue. Create a pivot table to
   compute mean Revenue for each Quarter by Year.
"""

import numpy as np
import pandas as pd


def value_by_date_category_pivot():
    rng = np.random.default_rng(42)
    dates = pd.date_range(start="2021-01-01", periods=6, freq="D")
    df = pd.DataFrame(
        {
            "Date": np.repeat(dates, 3),
            "Category": ["A", "B", "C"] * len(dates),
            "Value": rng.integers(10, 101, size=len(dates) * 3),
        }
    )
    pivot = pd.pivot_table(df, values="Value", index="Date", columns="Category", aggfunc="sum")
    return df, pivot


def revenue_by_year_quarter_pivot():
    rng = np.random.default_rng(42)
    df = pd.DataFrame(
        {
            "Year": [2021, 2021, 2021, 2021, 2022, 2022, 2022, 2022],
            "Quarter": ["Q1", "Q2", "Q3", "Q4", "Q1", "Q2", "Q3", "Q4"],
            "Revenue": rng.integers(10000, 50000, size=8),
        }
    )
    pivot = pd.pivot_table(df, values="Revenue", index="Year", columns="Quarter", aggfunc="mean")
    return df, pivot


if __name__ == "__main__":
    df, pivot = value_by_date_category_pivot()
    print("Date Category DataFrame:")
    print(df)
    print("\nPivot table: sum of Value by Date and Category:")
    print(pivot)

    df, pivot = revenue_by_year_quarter_pivot()
    print("\nRevenue DataFrame:")
    print(df)
    print("\nPivot table: mean Revenue by Year and Quarter:")
    print(pivot)
