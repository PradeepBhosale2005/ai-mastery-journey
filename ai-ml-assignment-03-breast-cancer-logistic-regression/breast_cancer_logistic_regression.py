from __future__ import annotations

from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import auc, classification_report, confusion_matrix, roc_curve
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def run_workflow(save_plot: bool = True, output_dir: str | Path = "outputs") -> Dict[str, object]:
    dataset = load_breast_cancer()
    x_train, x_test, y_train, y_test = train_test_split(
        dataset.data,
        dataset.target,
        test_size=0.2,
        random_state=42,
        stratify=dataset.target,
    )

    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)

    model = LogisticRegression(max_iter=5000, random_state=42)
    model.fit(x_train_scaled, y_train)

    predictions = model.predict(x_test_scaled)
    probabilities = model.predict_proba(x_test_scaled)[:, 1]

    matrix = confusion_matrix(y_test, predictions)
    report = classification_report(y_test, predictions, target_names=dataset.target_names, output_dict=True)
    fpr, tpr, thresholds = roc_curve(y_test, probabilities)
    auc_score = auc(fpr, tpr)

    plot_path = None
    if save_plot:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        plot_path = output_path / "roc_curve.png"
        plt.figure()
        plt.plot(fpr, tpr, label=f"AUC = {auc_score:.3f}")
        plt.plot([0, 1], [0, 1], linestyle="--")
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title("Breast Cancer Logistic Regression ROC Curve")
        plt.legend(loc="lower right")
        plt.tight_layout()
        plt.savefig(plot_path)
        plt.close()

    return {
        "train_size": len(x_train),
        "test_size": len(x_test),
        "confusion_matrix": matrix,
        "classification_report": report,
        "auc_score": float(auc_score),
        "roc_plot_path": str(plot_path) if plot_path else None,
        "threshold_count": len(thresholds),
    }


if __name__ == "__main__":
    result = run_workflow()
    print("Breast Cancer Logistic Regression workflow completed")
    print(f"Train size: {result['train_size']}")
    print(f"Test size: {result['test_size']}")
    print("Confusion Matrix:")
    print(result["confusion_matrix"])
    print("Classification Report:")
    for label, metrics in result["classification_report"].items():
        if isinstance(metrics, dict):
            print(f"{label}: precision={metrics['precision']:.3f}, recall={metrics['recall']:.3f}, f1={metrics['f1-score']:.3f}")
    print(f"ROC AUC Score: {result['auc_score']:.3f}")
    print(f"ROC curve saved to: {result['roc_plot_path']}")
