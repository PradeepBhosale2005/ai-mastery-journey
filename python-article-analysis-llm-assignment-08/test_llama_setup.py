import unittest

from main_llama import build_llama_chat_completions_url, parse_bool


class TestLlamaSetup(unittest.TestCase):
    def test_build_chat_completions_url_from_base(self):
        url = build_llama_chat_completions_url("https://example.com/v1")
        self.assertEqual(url, "https://example.com/v1/chat/completions")

    def test_build_chat_completions_url_does_not_duplicate_endpoint(self):
        url = build_llama_chat_completions_url("https://example.com/v1/chat/completions")
        self.assertEqual(url, "https://example.com/v1/chat/completions")

    def test_parse_bool_false_values(self):
        self.assertFalse(parse_bool("false"))
        self.assertFalse(parse_bool("0"))
        self.assertFalse(parse_bool("no"))

    def test_parse_bool_true_values(self):
        self.assertTrue(parse_bool("true"))
        self.assertTrue(parse_bool("1"))
        self.assertTrue(parse_bool("yes"))


if __name__ == "__main__":
    unittest.main()
