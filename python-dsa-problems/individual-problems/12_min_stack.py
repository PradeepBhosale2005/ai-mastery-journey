"""
Problem 12: Min Stack

Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.
"""


class MinStack:
    def __init__(self) -> None:
        self.items = []

    def push(self, val: int) -> None:
        current_min = val if not self.items else min(val, self.items[-1][1])
        self.items.append((val, current_min))

    def pop(self) -> None:
        if self.items:
            self.items.pop()

    def top(self) -> int:
        return self.items[-1][0]

    def getMin(self) -> int:
        return self.items[-1][1]


if __name__ == "__main__":
    min_stack = MinStack()
    min_stack.push(-2)
    min_stack.push(0)
    min_stack.push(-3)
    print(min_stack.getMin())
    min_stack.pop()
    print(min_stack.top())
    print(min_stack.getMin())
