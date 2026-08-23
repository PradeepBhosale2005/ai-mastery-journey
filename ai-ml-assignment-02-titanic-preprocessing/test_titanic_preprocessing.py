from titanic_preprocessing import load_titanic_data, preprocess_titanic_data, run_pipeline


def test_loads_required_columns():
    data = load_titanic_data()
    assert list(data.columns) == ["survived", "pclass", "sex", "age", "fare", "embarked"]
    assert len(data) > 0


def test_preprocessing_removes_missing_values_and_encodes_features():
    data = load_titanic_data()
    features, target, metadata = preprocess_titanic_data(data)
    assert features.isna().sum().sum() == 0
    assert target.name == "survived"
    assert "sex" in features.columns
    assert any(column.startswith("embarked_") for column in features.columns)
    assert metadata["missing_before"]["age"] > 0


def test_run_pipeline_outputs_expected_keys():
    result = run_pipeline()
    assert result["rows_loaded"] > 0
    assert result["train_shape"][0] > result["test_shape"][0]
    assert 0.0 <= result["test_accuracy"] <= 1.0
    assert "Random Forest" in result["cross_validation_scores"]
