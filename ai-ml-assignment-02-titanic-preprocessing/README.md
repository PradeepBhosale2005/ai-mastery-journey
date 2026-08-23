# AI-ML Assignment 02: Titanic Preprocessing Pipeline

This assignment converts Titanic passenger data into a clean numerical dataset suitable for machine learning.

## What it covers

- Load Titanic data
- Keep only required columns: `survived`, `pclass`, `sex`, `age`, `fare`, `embarked`
- Identify missing values
- Impute `age` using mean
- Impute `embarked` using mode
- Encode `sex` using Label Encoding
- Encode `embarked` using One-Hot Encoding
- Scale `age` and `fare` using StandardScaler
- Split into 80% train and 20% test using `random_state=42`
- Train a RandomForestClassifier
- Compare Logistic Regression, Random Forest, and KNN using cross-validation

## Run

```powershell
cd C:\Users\pradeep.bhosale_jade\ai-mastery-journey
cd .\ai-ml-assignment-02-titanic-preprocessing
python -m pip install -r requirements.txt
python titanic_preprocessing.py
```

## Test

```powershell
python test_titanic_preprocessing.py
```
