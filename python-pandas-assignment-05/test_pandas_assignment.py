import unittest

import numpy as np
import pandas as pd

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


class TestPandasAssignment(unittest.TestCase):
    def test_assignment_01(self):
        df = dataframe_with_first_column_as_index()
        self.assertEqual(df.shape, (6, 3))
        self.assertNotIn("ID", df.columns)

        df, value = access_element_by_label()
        self.assertEqual(value, df.loc["Y", "B"])

    def test_assignment_02(self):
        df = add_product_column()
        self.assertTrue((df["A_B_Product"] == df["A"] * df["B"]).all())

        df, row_sums, column_sums = compute_row_column_sums()
        self.assertTrue(row_sums.equals(df.sum(axis=1)))
        self.assertTrue(column_sums.equals(df.sum(axis=0)))

    def test_assignment_03(self):
        original, cleaned = fill_nan_with_column_mean()
        self.assertTrue(original.isna().any().any())
        self.assertFalse(cleaned.isna().any().any())

        original, cleaned = drop_rows_with_nan()
        self.assertTrue(original.isna().any().any())
        self.assertFalse(cleaned.isna().any().any())

    def test_assignment_04(self):
        df, grouped = category_value_aggregation()
        expected = df.groupby("Category")["Value"].agg(["sum", "mean"])
        pd.testing.assert_frame_equal(grouped, expected)

        df, total_sales = total_sales_by_category()
        expected = df.groupby("Category")["Sales"].sum()
        pd.testing.assert_series_equal(total_sales, expected)

    def test_assignment_05(self):
        students, marks, merged = merge_dataframes_on_common_column()
        self.assertEqual(len(merged), len(students))
        self.assertIn("Marks", merged.columns)

        df_one, df_two, concat_rows, concat_columns = concatenate_dataframes()
        self.assertEqual(concat_rows.shape[0], df_one.shape[0] + df_two.shape[0])
        self.assertEqual(concat_columns.shape[1], df_one.shape[1] + df_two.shape[1])

    def test_assignment_06(self):
        df, monthly_mean = monthly_mean_resample()
        self.assertFalse(monthly_mean.empty)
        self.assertEqual(df.index.freqstr, "D")

        rolling_df = seven_day_rolling_mean()
        self.assertIn("RollingMean7Days", rolling_df.columns)
        self.assertTrue(pd.isna(rolling_df["RollingMean7Days"].iloc[0]))

    def test_assignment_07(self):
        df, group_a, group_b_type_two = basic_multiindex_operations()
        self.assertIsInstance(df.index, pd.MultiIndex)
        self.assertEqual(len(group_a), 2)

        df, summed = category_subcategory_sum()
        self.assertIsInstance(df.index, pd.MultiIndex)
        self.assertFalse(summed.empty)

    def test_assignment_08(self):
        df, pivot = value_by_date_category_pivot()
        self.assertEqual(set(pivot.columns), set(df["Category"].unique()))

        df, pivot = revenue_by_year_quarter_pivot()
        self.assertEqual(set(pivot.columns), set(df["Quarter"].unique()))

    def test_assignment_09(self):
        df, doubled = double_dataframe_values()
        self.assertTrue((doubled == df * 2).all().all())

        df = add_row_sum_column()
        self.assertTrue((df["RowSum"] == df[["A", "B", "C"]].sum(axis=1)).all())

    def test_assignment_10(self):
        series, uppercase = convert_strings_to_uppercase()
        self.assertTrue((uppercase == series.str.upper()).all())

        series, first_three = extract_first_three_characters()
        self.assertTrue((first_three == series.str[:3]).all())


if __name__ == "__main__":
    unittest.main()
