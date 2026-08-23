from __future__ import annotations

from typing import Dict, List

import torch
import torch.nn as nn
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


class IrisMLP(nn.Module):
    def __init__(self, input_size: int = 4, hidden_size: int = 16, output_size: int = 3):
        super().__init__()
        self.hidden = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.output = nn.Linear(hidden_size, output_size)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.hidden(x)
        x = self.relu(x)
        x = self.output(x)
        return x


def prepare_data(test_size: float = 0.2, random_state: int = 42):
    iris = load_iris()
    x_train, x_test, y_train, y_test = train_test_split(
        iris.data,
        iris.target,
        test_size=test_size,
        random_state=random_state,
        stratify=iris.target,
    )

    scaler = StandardScaler()
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)

    x_train_tensor = torch.tensor(x_train, dtype=torch.float32)
    x_test_tensor = torch.tensor(x_test, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train, dtype=torch.long)
    y_test_tensor = torch.tensor(y_test, dtype=torch.long)

    return x_train_tensor, x_test_tensor, y_train_tensor, y_test_tensor


def train_model(epochs: int = 80, learning_rate: float = 0.01) -> Dict[str, object]:
    torch.manual_seed(42)
    x_train, x_test, y_train, y_test = prepare_data()

    model = IrisMLP()
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    losses: List[float] = []
    for epoch in range(1, epochs + 1):
        model.train()
        optimizer.zero_grad()
        outputs = model(x_train)
        loss = criterion(outputs, y_train)
        loss.backward()
        optimizer.step()
        losses.append(float(loss.item()))
        if epoch == 1 or epoch % 20 == 0 or epoch == epochs:
            print(f"Epoch {epoch}/{epochs} - Loss: {loss.item():.4f}")

    model.eval()
    with torch.no_grad():
        logits = model(x_test)
        predictions = torch.argmax(logits, dim=1).numpy()
        accuracy = accuracy_score(y_test.numpy(), predictions)

    return {
        "model": model,
        "losses": losses,
        "accuracy": float(accuracy),
        "test_count": len(y_test),
    }


if __name__ == "__main__":
    result = train_model()
    print(f"Test samples: {result['test_count']}")
    print(f"Classification accuracy: {result['accuracy']:.3f}")
