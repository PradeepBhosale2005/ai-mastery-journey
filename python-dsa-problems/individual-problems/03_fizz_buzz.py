"""
Problem 3: Fizz Buzz

Iterate from 1 to n and return a list where multiples of 3 are "Fizz",
multiples of 5 are "Buzz", and multiples of both 3 and 5 are "FizzBuzz".
"""

from typing import List


def fizz_buzz(n: int) -> List[str]:
    result = []

    for number in range(1, n + 1):
        if number % 15 == 0:
            result.append("FizzBuzz")
        elif number % 3 == 0:
            result.append("Fizz")
        elif number % 5 == 0:
            result.append("Buzz")
        else:
            result.append(str(number))

    return result


if __name__ == "__main__":
    n = 15
    print(fizz_buzz(n))
