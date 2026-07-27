import unittest

import numpy as np

from data_loader import load_processed_dataset
from linear_regression_scratch import train_custom_linear_regression
from linear_regression_sklearn import train_sklearn_linear_regression


class TestLinearRegressionAssignment(unittest.TestCase):
    def test_dataset_loads_correctly(self):
        X, y, df = load_processed_dataset()
        self.assertEqual(X.shape[1], 3)
        self.assertEqual(len(X), len(y))
        self.assertFalse(df.isna().any().any())

    def test_sklearn_model_trains(self):
        model, predictions, mse, r2 = train_sklearn_linear_regression()
        self.assertEqual(len(model.coef_), 3)
        self.assertLess(mse, 10)
        self.assertGreater(r2, 0.95)
        self.assertEqual(len(predictions), 60)

    def test_custom_model_trains(self):
        model, predictions, mse = train_custom_linear_regression()
        self.assertEqual(len(model.coefficients_), 3)
        self.assertLess(mse, 10)
        self.assertEqual(len(predictions), 60)

    def test_custom_coefficients_are_close_to_sklearn(self):
        sklearn_model, _, sklearn_mse, _ = train_sklearn_linear_regression()
        custom_model, _, custom_mse = train_custom_linear_regression()

        self.assertTrue(np.allclose(sklearn_model.coef_, custom_model.coefficients_, atol=1e-2))
        self.assertAlmostEqual(sklearn_model.intercept_, custom_model.intercept_, places=2)
        self.assertAlmostEqual(sklearn_mse, custom_mse, places=2)


if __name__ == "__main__":
    unittest.main()
