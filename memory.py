import json
import os
import tempfile
from copy import deepcopy
from pathlib import Path

DEFAULT_MEMORY = {
    "user_name": "Nanda",
    "facts": [],
    "preferences": [],
    "recent_topics": [],
}
MEMORY_FILE = Path(os.getenv("ASSISTANT_MEMORY_FILE", Path(__file__).with_name("memory.json")))
MAX_FACTS = 100
MAX_FACT_LENGTH = 500


def _normalize_memory(data):
    if not isinstance(data, dict):
        raise ValueError("Memory file must contain a JSON object.")

    normalized = deepcopy(DEFAULT_MEMORY)
    name = data.get("user_name", normalized["user_name"])
    if isinstance(name, str):
        normalized["user_name"] = name[:100]

    for key in ("facts", "preferences", "recent_topics"):
        values = data.get(key, [])
        if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
            raise ValueError(f"Memory field '{key}' must be a list of strings.")
        normalized[key] = [item[:MAX_FACT_LENGTH] for item in values[-MAX_FACTS:]]
    return normalized


def load_memory():
    if not MEMORY_FILE.exists():
        return deepcopy(DEFAULT_MEMORY)
    try:
        with MEMORY_FILE.open("r", encoding="utf-8") as memory_file:
            return _normalize_memory(json.load(memory_file))
    except (json.JSONDecodeError, OSError, ValueError) as error:
        raise ValueError(f"Could not read assistant memory at {MEMORY_FILE}: {error}") from error


def save_memory(memory_data):
    normalized = _normalize_memory(memory_data)
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=MEMORY_FILE.parent,
            delete=False,
        ) as memory_file:
            json.dump(normalized, memory_file, indent=2, ensure_ascii=False)
            memory_file.write("\n")
            temporary_path = Path(memory_file.name)
        temporary_path.replace(MEMORY_FILE)
    finally:
        if temporary_path and temporary_path.exists():
            temporary_path.unlink()


def clear_memory():
    save_memory(deepcopy(DEFAULT_MEMORY))


def add_fact(fact):
    fact = fact.strip()
    if not fact:
        return False
    if len(fact) > MAX_FACT_LENGTH:
        raise ValueError(f"Memory facts must be {MAX_FACT_LENGTH} characters or fewer.")

    memory = load_memory()
    if any(existing.casefold() == fact.casefold() for existing in memory["facts"]):
        return False
    memory["facts"].append(fact)
    memory["facts"] = memory["facts"][-MAX_FACTS:]
    save_memory(memory)
    return True


def add_recent_topic(topic):
    topic = topic.strip()
    if not topic:
        return
    memory = load_memory()
    topics = [item for item in memory["recent_topics"] if item.casefold() != topic.casefold()]
    topics.append(topic[:MAX_FACT_LENGTH])
    memory["recent_topics"] = topics[-10:]
    save_memory(memory)


def memory_as_text():
    memory = load_memory()
    return (
        f"User name: {memory['user_name']}\n"
        f"Facts: {', '.join(memory['facts'])}\n"
        f"Preferences: {', '.join(memory['preferences'])}\n"
        f"Recent topics: {', '.join(memory['recent_topics'])}"
    )
