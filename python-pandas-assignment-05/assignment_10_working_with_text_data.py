"""
Assignment 10: Working with Text Data

1. Create a Pandas Series with 5 random text strings and convert all strings to uppercase.
2. Create a Pandas Series with 5 random text strings and extract the first three characters.
"""

import pandas as pd


def convert_strings_to_uppercase():
    series = pd.Series(["apple", "banana", "cherry", "date", "elderberry"])
    uppercase_series = series.str.upper()
    return series, uppercase_series


def extract_first_three_characters():
    series = pd.Series(["python", "pandas", "numpy", "matrix", "dataset"])
    first_three = series.str[:3]
    return series, first_three


if __name__ == "__main__":
    series, uppercase = convert_strings_to_uppercase()
    print("Original Series:")
    print(series)
    print("\nUppercase Series:")
    print(uppercase)

    series, first_three = extract_first_three_characters()
    print("\nOriginal Series:")
    print(series)
    print("\nFirst three characters:")
    print(first_three)
