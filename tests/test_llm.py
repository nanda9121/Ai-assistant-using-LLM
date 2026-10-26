import io
import json
import unittest
from unittest.mock import patch

from llm import OllamaError, ask_ai, build_prompt


class LlmTests(unittest.TestCase):
    def test_prompt_includes_memory_context_and_user_request(self):
        prompt = build_prompt("hello", "likes tea", "tea facts")
        self.assertIn("likes tea", prompt)
        self.assertIn("tea facts", prompt)
        self.assertIn("hello", prompt)

    def test_ask_ai_returns_trimmed_response(self):
        response_body = json.dumps({"response": "  Hello there.  "}).encode()
        response = io.BytesIO(response_body)
        with patch("llm.urlopen", return_value=response) as urlopen:
            answer = ask_ai("hello")

        self.assertEqual(answer, "Hello there.")
        self.assertEqual(urlopen.call_args.kwargs["timeout"], 60)

    def test_missing_model_has_actionable_message(self):
        from urllib.error import HTTPError

        response = io.BytesIO(b"model not found")
        error = HTTPError(
            "http://localhost:11434/api/generate",
            404,
            "Not Found",
            {},
            response,
        )
        with patch("llm.urlopen", side_effect=error):
            with self.assertRaisesRegex(OllamaError, "ollama pull llama3"):
                ask_ai("hello")
        error.close()

    def test_empty_user_input_is_rejected(self):
        with self.assertRaises(ValueError):
            ask_ai(" ")


if __name__ == "__main__":
    unittest.main()
