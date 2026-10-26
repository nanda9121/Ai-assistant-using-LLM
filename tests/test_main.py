import unittest
from unittest.mock import call, patch

import main


class MainTests(unittest.TestCase):
    def test_text_mode_routes_questions_to_llm_and_remembers_topics(self):
        inputs = iter(["Explain HTTP APIs", "exit"])
        with (
            patch("builtins.input", side_effect=lambda _: next(inputs)),
            patch.object(main, "ask_ai", return_value="An API connects software.") as ask_ai,
            patch.object(main, "memory_as_text", return_value="User name: Nanda"),
            patch.object(main, "retrieve_context", return_value="API notes") as retrieve_context,
            patch.object(main, "add_recent_topic") as add_recent_topic,
            patch("builtins.print") as print_output,
        ):
            result = main.run_assistant(text_mode=True)

        self.assertEqual(result, 0)
        ask_ai.assert_called_once_with(
            user_input="Explain HTTP APIs",
            memory_text="User name: Nanda",
            retrieved_context="API notes",
        )
        retrieve_context.assert_called_once_with("Explain HTTP APIs")
        add_recent_topic.assert_called_once_with("Explain HTTP APIs")
        print_output.assert_has_calls([
            call("JARVIS is ready. Ask a question or say help."),
            call("An API connects software."),
            call("Shutting down the assistant. Goodbye."),
        ])

    def test_text_mode_can_save_a_memory_fact(self):
        inputs = iter(["remember that I like Python", "exit"])
        with (
            patch("builtins.input", side_effect=lambda _: next(inputs)),
            patch.object(main, "add_fact", return_value=True) as add_fact,
            patch("builtins.print"),
        ):
            result = main.run_assistant(text_mode=True)

        self.assertEqual(result, 0)
        add_fact.assert_called_once_with("i like python")


if __name__ == "__main__":
    unittest.main()
