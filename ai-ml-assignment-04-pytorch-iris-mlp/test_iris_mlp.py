import torch

from iris_mlp import IrisMLP, prepare_data, train_model


def test_model_forward_shape():
    model = IrisMLP()
    sample = torch.randn(5, 4)
    output = model(sample)
    assert output.shape == (5, 3)


def test_prepare_data_shapes():
    x_train, x_test, y_train, y_test = prepare_data()
    assert x_train.shape[1] == 4
    assert x_test.shape[1] == 4
    assert y_train.dtype == torch.long
    assert y_test.dtype == torch.long


def test_training_runs_for_small_epoch_count():
    result = train_model(epochs=2)
    assert len(result["losses"]) == 2
    assert 0.0 <= result["accuracy"] <= 1.0
