from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler

REQUIRED_COLUMNS = ["survived", "pclass", "sex", "age", "fare", "embarked"]


def load_titanic_data(csv_path: str | Path = "data/titanic_sample.csv") -> pd.DataFrame:
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"Titanic CSV not found: {path}")
    data = pd.read_csv(path)
    return data[REQUIRED_COLUMNS].copy()


def identify_missing_values(data: pd.DataFrame) -> pd.Series:
    return data.isna().sum()


def preprocess_titanic_data(data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series, Dict[str, object]]:
    working = data[REQUIRED_COLUMNS].copy()
    missing_before = identify_missing_values(working)

    age_mean = working["age"].mean()
    embarked_mode = working["embarked"].mode(dropna=True)[0]

    working["age"] = working["age"].fillna(age_mean)
    working["embarked"] = working["embarked"].fillna(embarked_mode)

    sex_encoder = LabelEncoder()
    working["sex"] = sex_encoder.fit_transform(working["sex"])

    working = pd.get_dummies(working, columns=["embarked"], prefix="embarked", dtype=int)

    scaler = StandardScaler()
    working[["age", "fare"]] = scaler.fit_transform(working[["age", "fare"]])

    target = working["survived"]
    features = working.drop(columns=["survived"])

    metadata = {
        "missing_before": missing_before.to_dict(),
        "age_mean_used": float(age_mean),
        "embarked_mode_used": embarked_mode,
        "sex_classes": list(sex_encoder.classes_),
        "feature_columns": list(features.columns),
    }
    return features, target, metadata


def split_data(features: pd.DataFrame, target: pd.Series):
    return train_test_split(features, target, test_size=0.2, random_state=42, stratify=target)


def compare_models(features: pd.DataFrame, target: pd.Series) -> Dict[str, float]:
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Random Forest": RandomForestClassifier(n_estimators=50, random_state=42),
        "KNN": KNeighborsClassifier(n_neighbors=3),
    }
    scores: Dict[str, float] = {}
    for name, model in models.items():
        cv_scores = cross_val_score(model, features, target, cv=3, scoring="accuracy")
        scores[name] = float(cv_scores.mean())
    return scores


def run_pipeline(csv_path: str | Path = "data/titanic_sample.csv") -> Dict[str, object]:
    raw_data = load_titanic_data(csv_path)
    features, target, metadata = preprocess_titanic_data(raw_data)
    x_train, x_test, y_train, y_test = split_data(features, target)

    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)

    result = {
        "rows_loaded": len(raw_data),
        "missing_before": metadata["missing_before"],
        "feature_columns": metadata["feature_columns"],
        "train_shape": x_train.shape,
        "test_shape": x_test.shape,
        "test_accuracy": float(accuracy_score(y_test, predictions)),
        "cross_validation_scores": compare_models(features, target),
    }
    return result


if __name__ == "__main__":
    output = run_pipeline()
    print("Titanic preprocessing and model pipeline completed")
    print(f"Rows loaded: {output['rows_loaded']}")
    print(f"Missing values before preprocessing: {output['missing_before']}")
    print(f"Feature columns: {output['feature_columns']}")
    print(f"Train shape: {output['train_shape']}")
    print(f"Test shape: {output['test_shape']}")
    print(f"Test accuracy: {output['test_accuracy']:.3f}")
    print("Cross-validation comparison:")
    for model_name, score in output["cross_validation_scores"].items():
        print(f"- {model_name}: {score:.3f}")
