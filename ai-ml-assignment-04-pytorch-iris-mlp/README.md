# AI-ML Assignment 04: PyTorch Iris Feed-Forward Neural Network

This assignment implements a basic feed-forward neural network using PyTorch for Iris classification.

## What it covers

- Load Iris dataset
- Split data into train and test sets
- Scale features
- Convert arrays into PyTorch tensors
- Create a model by inheriting from `torch.nn.Module`
- Manually implement the `forward()` method
- Use one hidden layer with ReLU activation
- Train using CrossEntropyLoss and Adam optimizer
- Print loss during training
- Evaluate classification accuracy on the test set

## Run

```powershell
cd C:\Users\pradeep.bhosale_jade\ai-mastery-journey
cd .\ai-ml-assignment-04-pytorch-iris-mlp
python -m pip install -r requirements.txt
python iris_mlp.py
```

## Test

```powershell
python test_iris_mlp.py
```
