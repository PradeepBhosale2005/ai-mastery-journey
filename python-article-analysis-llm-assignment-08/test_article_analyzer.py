import json
import unittest

from article_analyzer import (
    ResponseValidationError,
    analyze_article_from_raw_response,
    build_prompt,
    extract_text_from_api_response,
    validate_analysis_json,
)


VALID_RESPONSE = {
    "summary": "This is a concise summary of the article within the allowed word limit.",
    "important_points": [
        "Point one captures an important idea.",
        "Point two captures an important idea.",
        "Point three captures an important idea.",
        "Point four captures an important idea.",
        "Point five captures an important idea.",
    ],
    "key_themes": ["Theme one", "Theme two", "Theme three"],
    "target_audience": "Professionals and readers interested in the article topic.",
}


class TestArticleAnalyzer(unittest.TestCase):
    def test_prompt_contains_required_json_fields(self):
        prompt = build_prompt("Sample article text")
        self.assertIn("summary", prompt)
        self.assertIn("important_points", prompt)
        self.assertIn("key_themes", prompt)
        self.assertIn("target_audience", prompt)
        self.assertIn("Do not include markdown", prompt)

    def test_valid_response_passes_validation(self):
        validated = validate_analysis_json(VALID_RESPONSE)
        self.assertEqual(validated["summary"], VALID_RESPONSE["summary"])

    def test_raw_json_response_is_parsed_and_validated(self):
        raw_response = json.dumps(VALID_RESPONSE)
        parsed = analyze_article_from_raw_response(raw_response)
        self.assertEqual(parsed["key_themes"], VALID_RESPONSE["key_themes"])

    def test_missing_required_field_fails_validation(self):
        invalid_response = dict(VALID_RESPONSE)
        invalid_response.pop("target_audience")

        with self.assertRaises(ResponseValidationError):
            validate_analysis_json(invalid_response)

    def test_too_few_important_points_fails_validation(self):
        invalid_response = dict(VALID_RESPONSE)
        invalid_response["important_points"] = ["Only one point"]

        with self.assertRaises(ResponseValidationError):
            validate_analysis_json(invalid_response)

    def test_too_many_key_themes_fails_validation(self):
        invalid_response = dict(VALID_RESPONSE)
        invalid_response["key_themes"] = [
            "Theme one",
            "Theme two",
            "Theme three",
            "Theme four",
            "Theme five",
            "Theme six",
        ]

        with self.assertRaises(ResponseValidationError):
            validate_analysis_json(invalid_response)

    def test_summary_over_150_words_fails_validation(self):
        invalid_response = dict(VALID_RESPONSE)
        invalid_response["summary"] = "word " * 151

        with self.assertRaises(ResponseValidationError):
            validate_analysis_json(invalid_response)

    def test_malformed_json_fails_gracefully(self):
        with self.assertRaises(ResponseValidationError):
            analyze_article_from_raw_response("This is not JSON")

    def test_extract_text_from_openai_style_response(self):
        api_response = {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(VALID_RESPONSE)
                    }
                }
            ]
        }
        extracted = extract_text_from_api_response(api_response)
        self.assertEqual(json.loads(extracted), VALID_RESPONSE)


if __name__ == "__main__":
    unittest.main()
