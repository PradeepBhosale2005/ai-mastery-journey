"""
Problem 5: Valid Palindrome

Check if a string is a palindrome after removing non-alphanumeric characters
and ignoring the case.
"""


def is_valid_palindrome(s: str) -> bool:
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


if __name__ == "__main__":
    text = "A man, a plan, a canal: Panama"
    print(is_valid_palindrome(text))
