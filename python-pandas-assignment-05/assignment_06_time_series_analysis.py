"""
Assignment 6: Time Series Analysis

1. Create a DataFrame with a datetime index and one random integer column.
   Resample it to compute monthly mean.
2. Create a DataFrame with datetime index from 2021-01-01 to 2021-12-31.
   Compute rolling mean with a window of 7 days.
"""

import numpy as np
import pandas as pd


def monthly_mean_resample():
    rng = np.random.default_rng(42)
    dates = pd.date_range(start="2021-01-01", periods=120, freq="D")
    df = pd.DataFrame({"Value": rng.integers(1, 101, size=len(dates))}, index=dates)
    monthly_mean = df.resample("ME").mean()
    return df, monthly_mean


def seven_day_rolling_mean():
    rng = np.random.default_rng(42)
    dates = pd.date_range(start="2021-01-01", end="2021-12-31", freq="D")
    df = pd.DataFrame({"Value": rng.integers(1, 101, size=len(dates))}, index=dates)
    df["RollingMean7Days"] = df["Value"].rolling(window=7).mean()
    return df


if __name__ == "__main__":
    df, monthly_mean = monthly_mean_resample()
    print("Daily DataFrame sample:")
    print(df.head())
    print("\nMonthly mean:")
    print(monthly_mean)

    rolling_df = seven_day_rolling_mean()
    print("\n7-day rolling mean sample:")
    print(rolling_df.head(10))
