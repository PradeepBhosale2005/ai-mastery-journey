"""
Run all Pandas assignment sections from one script.
"""

from assignment_01_dataframe_creation_indexing import access_element_by_label, dataframe_with_first_column_as_index
from assignment_02_dataframe_operations import add_product_column, compute_row_column_sums
from assignment_03_data_cleaning import drop_rows_with_nan, fill_nan_with_column_mean
from assignment_04_data_aggregation import category_value_aggregation, total_sales_by_category
from assignment_05_merging_dataframes import concatenate_dataframes, merge_dataframes_on_common_column
from assignment_06_time_series_analysis import monthly_mean_resample, seven_day_rolling_mean
from assignment_07_multiindex_dataframe import basic_multiindex_operations, category_subcategory_sum
from assignment_08_pivot_tables import revenue_by_year_quarter_pivot, value_by_date_category_pivot
from assignment_09_applying_functions import add_row_sum_column, double_dataframe_values
from assignment_10_working_with_text_data import convert_strings_to_uppercase, extract_first_three_characters


def show(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


if __name__ == "__main__":
    show("Assignment 1: DataFrame Creation and Indexing")
    print(dataframe_with_first_column_as_index())
    print(access_element_by_label())

    show("Assignment 2: DataFrame Operations")
    print(add_product_column())
    print(compute_row_column_sums())

    show("Assignment 3: Data Cleaning")
    print(fill_nan_with_column_mean())
    print(drop_rows_with_nan())

    show("Assignment 4: Data Aggregation")
    print(category_value_aggregation())
    print(total_sales_by_category())

    show("Assignment 5: Merging DataFrames")
    print(merge_dataframes_on_common_column())
    print(concatenate_dataframes())

    show("Assignment 6: Time Series Analysis")
    print(monthly_mean_resample())
    print(seven_day_rolling_mean().head(10))

    show("Assignment 7: MultiIndex DataFrame")
    print(basic_multiindex_operations())
    print(category_subcategory_sum())

    show("Assignment 8: Pivot Tables")
    print(value_by_date_category_pivot())
    print(revenue_by_year_quarter_pivot())

    show("Assignment 9: Applying Functions")
    print(double_dataframe_values())
    print(add_row_sum_column())

    show("Assignment 10: Working with Text Data")
    print(convert_strings_to_uppercase())
    print(extract_first_three_characters())
