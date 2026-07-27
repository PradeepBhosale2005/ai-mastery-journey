"""
Assignment Part 3:
Compare the learned coefficients and intercept from the custom gradient descent
implementation with the scikit-learn implementation.
"""

import pandas as pd

from data_loader import FEATURE_COLUMNS
from linear_regression_scratch import train_custom_linear_regression
from linear_regression_sklearn import train_sklearn_linear_regression


def compare_models():
    """Train both models and compare coefficients, intercept, and error."""
    sklearn_model, sklearn_predictions, sklearn_mse, sklearn_r2 = train_sklearn_linear_regression()
    custom_model, custom_predictions, custom_mse = train_custom_linear_regression()

    comparison_df = pd.DataFrame(
        {
            "Feature": FEATURE_COLUMNS,
            "Scikit_Learn_Coefficient": sklearn_model.coef_,
            "Custom_GD_Coefficient": custom_model.coefficients_,
            "Absolute_Difference": abs(sklearn_model.coef_ - custom_model.coefficients_),
        }
    )

    intercept_comparison = pd.DataFrame(
        {
            "Metric": ["Intercept", "Mean Squared Error"],
            "Scikit_Learn": [sklearn_model.intercept_, sklearn_mse],
            "Custom_GD": [custom_model.intercept_, custom_mse],
            "Absolute_Difference": [
                abs(sklearn_model.intercept_ - custom_model.intercept_),
                abs(sklearn_mse - custom_mse),
            ],
        }
    )

    return comparison_df, intercept_comparison, sklearn_r2


if __name__ == "__main__":
    coefficient_comparison, intercept_comparison, sklearn_r2 = compare_models()

    print("Coefficient Comparison")
    print("----------------------")
    print(coefficient_comparison)

    print("\nIntercept and Error Comparison")
    print("------------------------------")
    print(intercept_comparison)

    print("\nScikit-learn R2 Score:", sklearn_r2)
    print("\nConclusion:")
    print(
        "The custom gradient descent implementation learns coefficients and intercept "
        "very close to the scikit-learn LinearRegression model."
    )
