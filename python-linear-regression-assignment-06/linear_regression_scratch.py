"""
Assignment Part 2:
Implement Linear Regression from scratch using gradient descent.

No machine learning library is used for the custom model.
NumPy is used only for numerical array operations.
"""

import numpy as np

from data_loader import FEATURE_COLUMNS, load_processed_dataset


class LinearRegressionFromScratch:
    """Linear Regression model implemented from scratch using gradient descent."""

    def __init__(self, learning_rate: float = 0.05, epochs: int = 20000) -> None:
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.weights = None
        self.bias = 0.0
        self.feature_means = None
        self.feature_stds = None
        self.coefficients_ = None
        self.intercept_ = None
        self.loss_history = []

    def _standardize_features(self, X: np.ndarray) -> np.ndarray:
        """Standardize features for stable gradient descent."""
        return (X - self.feature_means) / self.feature_stds

    def fit(self, X: np.ndarray, y: np.ndarray):
        """Train the model using batch gradient descent."""
        X = np.asarray(X, dtype=float)
        y = np.asarray(y, dtype=float)

        self.feature_means = X.mean(axis=0)
        self.feature_stds = X.std(axis=0)
        self.feature_stds[self.feature_stds == 0] = 1

        X_scaled = self._standardize_features(X)
        number_of_samples, number_of_features = X_scaled.shape

        self.weights = np.zeros(number_of_features)
        self.bias = 0.0

        for _ in range(self.epochs):
            predictions = np.dot(X_scaled, self.weights) + self.bias
            errors = predictions - y

            dw = (2 / number_of_samples) * np.dot(X_scaled.T, errors)
            db = (2 / number_of_samples) * np.sum(errors)

            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

            loss = np.mean(errors ** 2)
            self.loss_history.append(loss)

        # Convert scaled coefficients back to the original feature scale.
        self.coefficients_ = self.weights / self.feature_stds
        self.intercept_ = self.bias - np.sum((self.weights * self.feature_means) / self.feature_stds)

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict target values using the trained model."""
        X = np.asarray(X, dtype=float)
        return np.dot(X, self.coefficients_) + self.intercept_


def train_custom_linear_regression():
    """Train the custom gradient descent model on the processed dataset."""
    X, y, _ = load_processed_dataset()

    model = LinearRegressionFromScratch(learning_rate=0.05, epochs=20000)
    model.fit(X, y)

    predictions = model.predict(X)
    mse = np.mean((predictions - y) ** 2)

    return model, predictions, mse


if __name__ == "__main__":
    model, predictions, mse = train_custom_linear_regression()

    print("Custom Linear Regression using Gradient Descent")
    print("------------------------------------------------")
    print("Feature columns:", FEATURE_COLUMNS)
    print("Coefficients:", model.coefficients_)
    print("Intercept:", model.intercept_)
    print("Mean Squared Error:", mse)
    print("Final training loss:", model.loss_history[-1])
    print("\nFirst 5 predictions:")
    print(predictions[:5])
