import argparse

from commands import handle_command
from llm import OllamaError, ask_ai
from memory import add_fact, add_recent_topic, clear_memory, memory_as_text
from retrieval import retrieve_context
from speech import listen, speak


def run_assistant(text_mode=False):
    respond = print if text_mode else speak
    respond("JARVIS is ready. Ask a question or say help.")

    while True:
        try:
            user_input = input("You: ").strip() if text_mode else listen()
        except (EOFError, KeyboardInterrupt):
            respond("Goodbye.")
            break
        except RuntimeError as error:
            respond(str(error))
            return 1

        if not user_input:
            continue

        command = user_input.casefold()
        if command in {"exit", "quit", "stop listening", "goodbye"}:
            respond("Shutting down the assistant. Goodbye.")
            break

        if command in {"clear memory", "forget everything"}:
            try:
                clear_memory()
            except (OSError, ValueError) as error:
                respond(f"I could not clear memory: {error}")
            else:
                respond("Memory cleared.")
            continue

        if command.startswith("remember that "):
            fact = command.removeprefix("remember that ").strip()
            try:
                added = add_fact(fact)
            except (OSError, ValueError) as error:
                respond(f"I could not save that memory: {error}")
            else:
                respond("I will remember that." if added else "I already have that in memory.")
            continue

        if command in {"what do you remember", "read my memory"}:
            try:
                respond(memory_as_text())
            except (OSError, ValueError) as error:
                respond(f"I could not read memory: {error}")
            continue

        try:
            command_response = handle_command(command)
        except (OSError, RuntimeError, ValueError) as error:
            respond(f"I could not complete that command: {error}")
            continue
        if command_response:
            respond(command_response)
            continue

        try:
            reply = ask_ai(
                user_input=user_input,
                memory_text=memory_as_text(),
                retrieved_context=retrieve_context(user_input),
            )
        except (OllamaError, OSError, ValueError) as error:
            respond(str(error))
            continue

        respond(reply)
        try:
            add_recent_topic(user_input)
        except (OSError, ValueError) as error:
            print(f"Could not save recent topic: {error}")

    return 0


def main():
    parser = argparse.ArgumentParser(description="Voice and text AI assistant powered by Ollama.")
    parser.add_argument(
        "--text",
        action="store_true",
        help="Use the terminal instead of a microphone and speaker.",
    )
    args = parser.parse_args()
    return run_assistant(text_mode=args.text)


if __name__ == "__main__":
    raise SystemExit(main())
