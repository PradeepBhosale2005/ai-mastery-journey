"""
Assignment 5: Merging DataFrames

1. Create two DataFrames with a common column and merge them using that column.
2. Create two DataFrames with different columns and concatenate them along rows
   and columns.
"""

import pandas as pd


def merge_dataframes_on_common_column():
    students = pd.DataFrame({"StudentID": [1, 2, 3], "Name": ["Amit", "Sneha", "Rahul"]})
    marks = pd.DataFrame({"StudentID": [1, 2, 3], "Marks": [88, 92, 79]})
    merged = pd.merge(students, marks, on="StudentID")
    return students, marks, merged


def concatenate_dataframes():
    df_one = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    df_two = pd.DataFrame({"C": [5, 6], "D": [7, 8]})
    concat_rows = pd.concat([df_one, df_two], axis=0, ignore_index=True)
    concat_columns = pd.concat([df_one, df_two], axis=1)
    return df_one, df_two, concat_rows, concat_columns


if __name__ == "__main__":
    students, marks, merged = merge_dataframes_on_common_column()
    print("Students DataFrame:")
    print(students)
    print("\nMarks DataFrame:")
    print(marks)
    print("\nMerged DataFrame:")
    print(merged)

    df_one, df_two, concat_rows, concat_columns = concatenate_dataframes()
    print("\nConcatenated along rows:")
    print(concat_rows)
    print("\nConcatenated along columns:")
    print(concat_columns)
