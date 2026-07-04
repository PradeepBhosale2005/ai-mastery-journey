import unittest

from solutions import (
    MinStack,
    contains_duplicate,
    convert_to_camel_case,
    fizz_buzz,
    group_anagrams,
    intersection,
    is_valid_palindrome,
    longest_common_prefix,
    longest_palindromic_substring,
    max_area,
    prime_factors,
    roman_to_int,
    top_k_frequent,
    two_sum,
)


class TestDSASolutions(unittest.TestCase):
    def test_contains_duplicate(self):
        self.assertTrue(contains_duplicate([1, 2, 3, 1]))
        self.assertFalse(contains_duplicate([1, 2, 3, 4]))

    def test_prime_factors(self):
        self.assertEqual(prime_factors(100), [2, 5])
        self.assertEqual(prime_factors(315), [3, 5, 7])
        self.assertEqual(prime_factors(1), [])

    def test_fizz_buzz(self):
        self.assertEqual(
            fizz_buzz(15),
            [
                "1",
                "2",
                "Fizz",
                "4",
                "Buzz",
                "Fizz",
                "7",
                "8",
                "Fizz",
                "Buzz",
                "11",
                "Fizz",
                "13",
                "14",
                "FizzBuzz",
            ],
        )

    def test_max_area(self):
        self.assertEqual(max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]), 49)

    def test_is_valid_palindrome(self):
        self.assertTrue(is_valid_palindrome("A man, a plan, a canal: Panama"))
        self.assertFalse(is_valid_palindrome("race a car"))

    def test_longest_common_prefix(self):
        self.assertEqual(longest_common_prefix(["flower", "flow", "flight"]), "fl")
        self.assertEqual(longest_common_prefix(["dog", "racecar", "car"]), "")

    def test_convert_to_camel_case(self):
        self.assertEqual(convert_to_camel_case("hello world from python"), "HelloWorldFromPython")
        self.assertEqual(convert_to_camel_case("  ai mastery journey  "), "AiMasteryJourney")

    def test_longest_palindromic_substring(self):
        self.assertIn(longest_palindromic_substring("babad"), ["bab", "aba"])
        self.assertEqual(longest_palindromic_substring("cbbd"), "bb")

    def test_group_anagrams(self):
        result = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
        sorted_groups = sorted([sorted(group) for group in result])
        expected = sorted([sorted(group) for group in [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]])
        self.assertEqual(sorted_groups, expected)

    def test_two_sum(self):
        self.assertEqual(two_sum([2, 7, 11, 15], 9), [0, 1])

    def test_top_k_frequent(self):
        self.assertEqual(set(top_k_frequent([1, 1, 1, 2, 2, 3], 2)), {1, 2})

    def test_min_stack(self):
        stack = MinStack()
        stack.push(-2)
        stack.push(0)
        stack.push(-3)
        self.assertEqual(stack.getMin(), -3)
        stack.pop()
        self.assertEqual(stack.top(), 0)
        self.assertEqual(stack.getMin(), -2)

    def test_intersection(self):
        self.assertEqual(intersection([1, 2, 2, 1], [2, 2]), [2])
        self.assertEqual(intersection([4, 9, 5], [9, 4, 9, 8, 4]), [4, 9])

    def test_roman_to_int(self):
        self.assertEqual(roman_to_int("III"), 3)
        self.assertEqual(roman_to_int("LVIII"), 58)
        self.assertEqual(roman_to_int("MCMXCIV"), 1994)


if __name__ == "__main__":
    unittest.main()
