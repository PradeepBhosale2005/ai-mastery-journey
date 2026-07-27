"""
Assignment Part 1:
Implement Linear Regression using the scikit-learn library and train it on the processed dataset.
"""

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

from data_loader import FEATURE_COLUMNS, load_processed_dataset


def train_sklearn_linear_regression():
    """Train LinearRegression from scikit-learn on the processed dataset."""
    X, y, _ = load_processed_dataset()

    model = LinearRegression()
    model.fit(X, y)

    predictions = model.predict(X)
    mse = mean_squared_error(y, predictions)
    r2 = r2_score(y, predictions)

    return model, predictions, mse, r2


if __name__ == "__main__":
    model, predictions, mse, r2 = train_sklearn_linear_regression()

    print("Scikit-learn Linear Regression")
    print("--------------------------------")
    print("Feature columns:", FEATURE_COLUMNS)
    print("Coefficients:", model.coef_)
    print("Intercept:", model.intercept_)
    print("Mean Squared Error:", mse)
    print("R2 Score:", r2)
    print("\nFirst 5 predictions:")
    print(predictions[:5])
