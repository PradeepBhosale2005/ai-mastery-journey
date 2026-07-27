# Linear Regression Assignment 06

## Assignment Summary

This assignment implements Linear Regression in two ways:

1. Using the `scikit-learn` library.
2. From scratch using custom batch gradient descent without using any machine learning library for the model.

The assignment also compares the learned coefficients and intercept from both implementations.

## Dataset

The processed dataset is included in:

```text
data/linear_regression_dataset.csv
```

The dataset contains 60 records with the following columns:

```text
study_hours
attendance_percent
previous_score
final_score
```

The target column is:

```text
final_score
```

The feature columns are:

```text
study_hours, attendance_percent, previous_score
```

## Learning Goals

- Train a Linear Regression model using scikit-learn.
- Implement Linear Regression from scratch.
- Understand the gradient descent update process.
- Compare coefficients and intercepts from two implementations.
- Evaluate the model using Mean Squared Error and R2 Score.

## Requirements

- Python installed on the system
- Visual Studio Code or any code editor
- NumPy
- Pandas
- scikit-learn
- Matplotlib

Install requirements using:

```bash
python -m pip install -r requirements.txt
```

If `python` does not work, try:

```bash
py -m pip install -r requirements.txt
```

Note: If `scikit-learn` installation fails on a very new Python version, use a stable Python version such as Python 3.11 or 3.12, or raise a JService ticket for Python/scikit-learn setup support.

## Project Structure

```text
python-linear-regression-assignment-06/
├── README.md
├── requirements.txt
├── data_loader.py
├── linear_regression_sklearn.py
├── linear_regression_scratch.py
├── compare_models.py
├── test_linear_regression.py
└── data/
    └── linear_regression_dataset.csv
```

## How to Run After Extracting ZIP File

### Step 1: Extract the ZIP File

Extract the submitted ZIP file on your system.

### Step 2: Open the Folder

Open the extracted folder in Visual Studio Code or any code editor.

### Step 3: Open Terminal

Open PowerShell, Command Prompt, or the integrated terminal in Visual Studio Code.

### Step 4: Go to the Assignment Folder

```bash
cd python-linear-regression-assignment-06
```

### Step 5: Install Requirements

```bash
python -m pip install -r requirements.txt
```

If `python` does not work, try:

```bash
py -m pip install -r requirements.txt
```

### Step 6: Run scikit-learn Linear Regression

```bash
python linear_regression_sklearn.py
```

### Step 7: Run Custom Gradient Descent Linear Regression

```bash
python linear_regression_scratch.py
```

### Step 8: Compare Both Models

```bash
python compare_models.py
```

This script prints:

- Scikit-learn coefficients
- Custom gradient descent coefficients
- Absolute coefficient differences
- Scikit-learn intercept
- Custom model intercept
- Mean Squared Error comparison

### Step 9: Run Test Cases

```bash
python test_linear_regression.py
```

If `python` does not work, try:

```bash
py test_linear_regression.py
```

Expected test result:

```text
OK
```

## Gradient Descent Formula Used

For a linear model:

```text
y_pred = Xw + b
```

The loss function is Mean Squared Error:

```text
MSE = mean((y_pred - y_actual)^2)
```

The gradient updates are:

```text
w = w - learning_rate * dw
b = b - learning_rate * db
```

## Assignment Status

Completed for the Linear Regression assignment in NEURALIS Phase 2.1.
