# AI-ML Assignment 05: PyTorch Handwritten Digit Classification

This assignment implements a PyTorch feed-forward neural network for handwritten digit classification.

The implementation uses the sklearn `load_digits` dataset. This keeps the assignment runnable without downloading external datasets.

## What it covers

- Load handwritten digit images
- Normalize image pixel values
- Flatten each image into a 1-D vector
- Split data into train and test sets
- Convert arrays into PyTorch tensors
- Create a model by inheriting from `torch.nn.Module`
- Manually implement the `forward()` method
- Use one hidden layer with ReLU activation
- Train using CrossEntropyLoss and Adam optimizer
- Print training loss during epochs
- Evaluate classification accuracy

## Run

```powershell
cd C:\Users\pradeep.bhosale_jade\ai-mastery-journey
cd .\ai-ml-assignment-05-pytorch-digits-mlp
python -m pip install -r requirements.txt
python digits_mlp.py
```

## Test

```powershell
python test_digits_mlp.py
```
