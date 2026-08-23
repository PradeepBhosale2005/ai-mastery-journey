from breast_cancer_logistic_regression import run_workflow


def test_workflow_returns_required_evaluation_outputs():
    result = run_workflow(save_plot=False)
    assert result["train_size"] > result["test_size"]
    assert result["confusion_matrix"].shape == (2, 2)
    assert "malignant" in result["classification_report"]
    assert 0.0 <= result["auc_score"] <= 1.0
    assert result["threshold_count"] > 0
