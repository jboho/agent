from typing import List

def format_history_block(history: List[str], suffix: str) -> str:
    """Formats history into LLM prompt-friendly string with given suffix."""
    return "\n".join([f"User: {msg}\n{suffix}: ..." for msg in history])
