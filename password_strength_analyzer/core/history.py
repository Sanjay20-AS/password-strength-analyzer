"""Safe local history: stores aggregate analysis metadata only."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

HISTORY_FILE = Path("password_history.json")

SAFE_FIELDS = {
    "timestamp", "score", "classification", "length", "estimated_entropy_bits",
    "common_password", "repeated_character", "sequential_pattern", "keyboard_pattern",
    "dictionary_word", "personal_information_overlap",
}


def save_safe_history(result: dict[str, Any], path: Path = HISTORY_FILE) -> None:
    """Persist only aggregate metadata. The password itself is never accepted or stored."""
    entry = {k: result[k] for k in SAFE_FIELDS if k in result}
    entry["timestamp"] = datetime.now(timezone.utc).isoformat()
    path.parent.mkdir(parents=True, exist_ok=True)

    records: list[dict[str, Any]] = []
    if path.exists():
        try:
            records = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(records, list):
                records = []
        except (json.JSONDecodeError, OSError):
            records = []
    records.append(entry)
    path.write_text(json.dumps(records[-50:], indent=2), encoding="utf-8")


def load_safe_history(path: Path = HISTORY_FILE) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def clear_history(path: Path = HISTORY_FILE) -> None:
    if path.exists():
        path.unlink()
