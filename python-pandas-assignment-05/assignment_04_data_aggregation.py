"""
Assignment 4: Data Aggregation

1. Create a DataFrame with Category and Value columns. Group by Category and
   compute sum and mean of Value.
2. Create a DataFrame with Product, Category, and Sales columns. Group by
   Category and compute total sales.
"""

import numpy as np
import pandas as pd


def category_value_aggregation():
    rng = np.random.default_rng(42)
    categories = rng.choice(["A", "B", "C"], size=12)
    values = rng.integers(10, 101, size=12)
    df = pd.DataFrame({"Category": categories, "Value": values})
    grouped = df.groupby("Category")["Value"].agg(["sum", "mean"])
    return df, grouped


def total_sales_by_category():
    rng = np.random.default_rng(42)
    products = ["Laptop", "Mouse", "Keyboard", "Monitor", "Chair", "Desk", "Tablet", "Phone"]
    categories = rng.choice(["Electronics", "Furniture", "Accessories"], size=len(products))
    sales = rng.integers(1000, 10000, size=len(products))
    df = pd.DataFrame({"Product": products, "Category": categories, "Sales": sales})
    total_sales = df.groupby("Category")["Sales"].sum()
    return df, total_sales


if __name__ == "__main__":
    df, grouped = category_value_aggregation()
    print("Category and Value DataFrame:")
    print(df)
    print("\nSum and mean by Category:")
    print(grouped)

    df, total_sales = total_sales_by_category()
    print("\nProduct Sales DataFrame:")
    print(df)
    print("\nTotal sales by Category:")
    print(total_sales)
