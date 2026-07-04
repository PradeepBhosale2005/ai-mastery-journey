"""
Problem 14: Roman to Integer

Convert a given Roman numeral string into an integer.
"""


def roman_to_int(s: str) -> int:
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
    roman_number = "LVIII"
    print(roman_to_int(roman_number))
