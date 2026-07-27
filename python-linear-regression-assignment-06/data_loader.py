"""
Utility functions for loading the processed linear regression dataset.
"""

from pathlib import Path

import pandas as pd


FEATURE_COLUMNS = ["study_hours", "attendance_percent", "previous_score"]
TARGET_COLUMN = "final_score"


def get_dataset_path() -> Path:
    """Return the path of the processed dataset CSV file."""
    return Path(__file__).parent / "data" / "linear_regression_dataset.csv"


def load_processed_dataset():
    """Load the processed dataset and return X, y, and the full DataFrame."""
    dataset_path = get_dataset_path()
    df = pd.read_csv(dataset_path)

    X = df[FEATURE_COLUMNS].to_numpy(dtype=float)
    y = df[TARGET_COLUMN].to_numpy(dtype=float)

    return X, y, df


if __name__ == "__main__":
    X, y, df = load_processed_dataset()
    print("Dataset loaded successfully")
    print("Dataset shape:", df.shape)
    print(df.head())
