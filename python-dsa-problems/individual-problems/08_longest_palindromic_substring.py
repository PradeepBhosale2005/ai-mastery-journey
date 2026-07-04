"""
Problem 8: Longest Palindromic Substring

Given a string S, return the longest palindromic substring in S.
"""


def longest_palindromic_substring(s: str) -> str:
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


if __name__ == "__main__":
    text = "babad"
    print(longest_palindromic_substring(text))
