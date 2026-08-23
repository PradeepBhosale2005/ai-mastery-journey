# AI-ML Assignment 03: Breast Cancer Logistic Regression

This assignment builds a complete sklearn machine learning workflow using the Breast Cancer dataset.

## What it covers

- Load the Breast Cancer dataset
- Split the data into 80% train and 20% test using `random_state=42`
- Apply `StandardScaler` to prevent feature-scale issues
- Train a Logistic Regression model
- Generate a confusion matrix
- Generate a classification report with precision, recall, and F1-score
- Analyze the malignant class
- Plot ROC curve and compute AUC score

## Run

```powershell
cd C:\Users\pradeep.bhosale_jade\ai-mastery-journey
cd .\ai-ml-assignment-03-breast-cancer-logistic-regression
python -m pip install -r requirements.txt
python breast_cancer_logistic_regression.py
```

## Test

```powershell
python test_breast_cancer_logistic_regression.py
```
