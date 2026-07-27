import unittest

from tokenizer import SimpleTokenizer


class TestSimpleTokenizer(unittest.TestCase):
    def test_tokenize_removes_punctuation_and_lowercases(self):
        tokenizer = SimpleTokenizer()
        tokens = tokenizer.tokenize("This is a test. This test is simple.")
        expected = ["this", "is", "a", "test", "this", "test", "is", "simple"]
        self.assertEqual(tokens, expected)

    def test_vocabulary_matches_assignment_example(self):
        tokenizer = SimpleTokenizer()
        tokens, token_ids, vocabulary = tokenizer.process_text(
            "This is a test. This test is simple."
        )

        expected_tokens = ["this", "is", "a", "test", "this", "test", "is", "simple"]
        expected_ids = [1, 2, 3, 4, 1, 4, 2, 5]
        expected_vocabulary = {
            "this": 1,
            "is": 2,
            "a": 3,
            "test": 4,
            "simple": 5,
        }

        self.assertEqual(tokens, expected_tokens)
        self.assertEqual(token_ids, expected_ids)
        self.assertEqual(vocabulary, expected_vocabulary)

    def test_existing_word_reuses_existing_id(self):
        tokenizer = SimpleTokenizer()
        tokenizer.process_text("This is a test.")
        token_ids = tokenizer.encode("This is another test.")

        self.assertEqual(token_ids[0], 1)
        self.assertEqual(token_ids[1], 2)
        self.assertEqual(token_ids[-1], 4)
        self.assertEqual(tokenizer.get_vocabulary()["another"], 5)

    def test_dynamic_vocabulary_update(self):
        tokenizer = SimpleTokenizer()
        tokenizer.process_text("This is a test.")
        tokenizer.process_text("This tokenizer is useful.")

        expected_vocabulary = {
            "this": 1,
            "is": 2,
            "a": 3,
            "test": 4,
            "tokenizer": 5,
            "useful": 6,
        }

        self.assertEqual(tokenizer.get_vocabulary(), expected_vocabulary)

    def test_process_multiple_sentences(self):
        tokenizer = SimpleTokenizer()
        tokens, token_ids, vocabulary = tokenizer.process_sentences(
            ["Python is simple.", "Python is powerful."]
        )

        self.assertEqual(tokens, ["python", "is", "simple", "python", "is", "powerful"])
        self.assertEqual(token_ids, [1, 2, 3, 1, 2, 4])
        self.assertEqual(vocabulary, {"python": 1, "is": 2, "simple": 3, "powerful": 4})

    def test_decode_ids_to_words(self):
        tokenizer = SimpleTokenizer()
        tokenizer.process_text("This is a test.")
        decoded = tokenizer.decode([1, 2, 3, 4])
        self.assertEqual(decoded, ["this", "is", "a", "test"])


if __name__ == "__main__":
    unittest.main()
