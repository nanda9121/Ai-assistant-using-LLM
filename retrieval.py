import os
import re
from pathlib import Path

KNOWLEDGE_FILE = Path(
    os.getenv("ASSISTANT_KNOWLEDGE_FILE", Path(__file__).with_name("knowledge.txt"))
)
WORD_PATTERN = re.compile(r"\b[\w'-]+\b", re.UNICODE)


def load_knowledge():
    if not KNOWLEDGE_FILE.exists():
        return []
    try:
        return [
            line.strip()
            for line in KNOWLEDGE_FILE.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
    except OSError as error:
        raise OSError(f"Could not read knowledge file at {KNOWLEDGE_FILE}: {error}") from error


def _tokens(text):
    return {word.casefold() for word in WORD_PATTERN.findall(text)}


def retrieve_context(query, top_k=3):
    if top_k <= 0:
        return ""

    query_words = _tokens(query)
    if not query_words:
        return ""

    scored = []
    for index, line in enumerate(load_knowledge()):
        line_words = _tokens(line)
        score = len(query_words & line_words)
        if score:
            scored.append((score, index, line))

    scored.sort(key=lambda entry: (-entry[0], entry[1]))
    return "\n".join(line for _, _, line in scored[:top_k])
