"""Tests for robust parsing of real hosted model outputs."""

import unittest

from validators_robust import parse_json_object, validate_turn_response


class TestRobustJsonParser(unittest.TestCase):
    def test_parses_markdown_fenced_json(self):
        parsed = parse_json_object('```json\n{"response": "AI customer support proposal"}\n```')
        self.assertEqual(validate_turn_response(parsed), "AI customer support proposal")

    def test_parses_inline_backtick_json(self):
        parsed = parse_json_object('`{"response": "AI customer support proposal"}`')
        self.assertEqual(validate_turn_response(parsed), "AI customer support proposal")

    def test_parses_json_after_thinking_block(self):
        raw = '<think>internal reasoning text</think>\n{"response": "AI customer support proposal"}'
        parsed = parse_json_object(raw)
        self.assertEqual(validate_turn_response(parsed), "AI customer support proposal")

    def test_parses_json_embedded_in_extra_text(self):
        raw = 'Here is the result:\n{"response": "AI customer support proposal"}\nDone.'
        parsed = parse_json_object(raw)
        self.assertEqual(validate_turn_response(parsed), "AI customer support proposal")

    def test_parses_escaped_json_string(self):
        raw = '"{\\"response\\": \\"AI customer support proposal\\"}"'
        parsed = parse_json_object(raw)
        self.assertEqual(validate_turn_response(parsed), "AI customer support proposal")


if __name__ == "__main__":
    unittest.main()
