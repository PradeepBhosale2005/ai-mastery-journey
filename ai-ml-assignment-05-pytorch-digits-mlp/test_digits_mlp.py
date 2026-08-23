import torch

from digits_mlp import DigitsMLP, prepare_data, train_model


def test_model_forward_shape():
    model = DigitsMLP()
    sample = torch.randn(4, 64)
    output = model(sample)
    assert output.shape == (4, 10)


def test_prepare_data_shapes():
    x_train, x_test, y_train, y_test = prepare_data()
    assert x_train.shape[1] == 64
    assert x_test.shape[1] == 64
    assert y_train.dtype == torch.long
    assert y_test.dtype == torch.long


def test_training_runs_for_small_epoch_count():
    result = train_model(epochs=2)
    assert len(result["losses"]) == 2
    assert 0.0 <= result["accuracy"] <= 1.0
