"""
Problem 2: Unique Prime Factors

Given a number n, find its unique prime factors in increasing order.
"""

from typing import List


def prime_factors(n: int) -> List[int]:
    factors = []

    if n < 2:
        return factors

    if n % 2 == 0:
        factors.append(2)
        while n % 2 == 0:
            n //= 2

    divisor = 3
    while divisor * divisor <= n:
        if n % divisor == 0:
            factors.append(divisor)
            while n % divisor == 0:
                n //= divisor
        divisor += 2

    if n > 1:
        factors.append(n)

    return factors


if __name__ == "__main__":
    n = 100
    print(prime_factors(n))
