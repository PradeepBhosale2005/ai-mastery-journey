"""
Python DSA Assignment Solutions

This file contains solutions for 14 array, string, stack, and number theory problems.
Each function is written so it can be imported and tested from test_solutions.py.
"""

from collections import Counter, defaultdict
from typing import List


# 1. Contains Duplicate
def contains_duplicate(nums: List[int]) -> bool:
    """Return True if any value appears at least twice; otherwise False."""
    return len(nums) != len(set(nums))


# 2. Unique Prime Factors in Increasing Order
def prime_factors(n: int) -> List[int]:
    """Return the unique prime factors of n in increasing order."""
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


# 3. Fizz Buzz
def fizz_buzz(n: int) -> List[str]:
    """Return Fizz, Buzz, FizzBuzz, or the number as a string from 1 to n."""
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


# 4. Container With Most Water
def max_area(height: List[int]) -> int:
    """Return the maximum water area formed by two vertical lines."""
    left = 0
    right = len(height) - 1
    best_area = 0

    while left < right:
        width = right - left
        current_height = min(height[left], height[right])
        best_area = max(best_area, width * current_height)

        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return best_area


# 5. Valid Palindrome
def is_valid_palindrome(s: str) -> bool:
    """Check if a string is a palindrome after ignoring case and non-alphanumeric chars."""
    left = 0
    right = len(s) - 1

    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1

        if s[left].lower() != s[right].lower():
            return False

        left += 1
        right -= 1

    return True


# 6. Longest Common Prefix
def longest_common_prefix(strings: List[str]) -> str:
    """Return the longest common prefix shared by all strings."""
    if not strings:
        return ""

    prefix = strings[0]

    for word in strings[1:]:
        while not word.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""

    return prefix


# 7. Convert Sentence to CamelCase
def convert_to_camel_case(sentence: str) -> str:
    """Convert a space-separated sentence to CamelCase."""
    words = sentence.split()
    return "".join(word[:1].upper() + word[1:].lower() for word in words)


# 8. Longest Palindromic Substring
def longest_palindromic_substring(s: str) -> str:
    """Return the longest palindromic substring in s."""
    if not s:
        return ""

    def expand_from_center(left: int, right: int) -> str:
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left + 1:right]

    longest = ""

    for index in range(len(s)):
        odd_palindrome = expand_from_center(index, index)
        even_palindrome = expand_from_center(index, index + 1)

        if len(odd_palindrome) > len(longest):
            longest = odd_palindrome
        if len(even_palindrome) > len(longest):
            longest = even_palindrome

    return longest


# 9. Group Anagrams
def group_anagrams(strings: List[str]) -> List[List[str]]:
    """Group anagrams together."""
    groups = defaultdict(list)

    for word in strings:
        key = tuple(sorted(word))
        groups[key].append(word)

    return list(groups.values())


# 10. Two Sum
def two_sum(nums: List[int], target: int) -> List[int]:
    """Return indices of two numbers that add up to target."""
    seen = {}

    for index, number in enumerate(nums):
        complement = target - number
        if complement in seen:
            return [seen[complement], index]
        seen[number] = index

    return []


# 11. Top K Frequent Elements
def top_k_frequent(nums: List[int], k: int) -> List[int]:
    """Return the k most frequent elements."""
    counts = Counter(nums)
    return [number for number, _ in counts.most_common(k)]


# 12. Min Stack
class MinStack:
    """Stack that supports push, pop, top, and retrieving the minimum in O(1)."""

    def __init__(self) -> None:
        self.stack = []

    def push(self, val: int) -> None:
        current_min = val if not self.stack else min(val, self.stack[-1][1])
        self.stack.append((val, current_min))

    def pop(self) -> None:
        if self.stack:
            self.stack.pop()

    def top(self) -> int:
        return self.stack[-1][0]

    def getMin(self) -> int:
        return self.stack[-1][1]

    def get_min(self) -> int:
        """Python-style alias for getMin."""
        return self.getMin()


# 13. Intersection of Two Arrays
def intersection(nums1: List[int], nums2: List[int]) -> List[int]:
    """Return the unique common elements between two arrays."""
    return sorted(list(set(nums1).intersection(set(nums2))))


# 14. Roman to Integer
def roman_to_int(s: str) -> int:
    """Convert a Roman numeral string to an integer."""
    values = {
        "I": 1,
        "V": 5,
        "X": 10,
        "L": 50,
        "C": 100,
        "D": 500,
        "M": 1000,
    }

    total = 0

    for index, symbol in enumerate(s):
        current_value = values[symbol]
        next_value = values[s[index + 1]] if index + 1 < len(s) else 0

        if current_value < next_value:
            total -= current_value
        else:
            total += current_value

    return total


if __name__ == "__main__":
    print("Contains duplicate:", contains_duplicate([1, 2, 3, 1]))
    print("Prime factors:", prime_factors(100))
    print("Fizz Buzz:", fizz_buzz(15))
    print("Max area:", max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]))
    print("Valid palindrome:", is_valid_palindrome("A man, a plan, a canal: Panama"))
    print("Longest common prefix:", longest_common_prefix(["flower", "flow", "flight"]))
    print("CamelCase:", convert_to_camel_case("hello world from python"))
    print("Longest palindromic substring:", longest_palindromic_substring("babad"))
    print("Group anagrams:", group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
    print("Two sum:", two_sum([2, 7, 11, 15], 9))
    print("Top K frequent:", top_k_frequent([1, 1, 1, 2, 2, 3], 2))

    min_stack = MinStack()
    min_stack.push(-2)
    min_stack.push(0)
    min_stack.push(-3)
    print("Min stack minimum:", min_stack.getMin())

    print("Intersection:", intersection([1, 2, 2, 1], [2, 2]))
    print("Roman to integer:", roman_to_int("LVIII"))
