from pathlib import Path

from password_strength_analyzer.core.analyzer import analyze_password
from password_strength_analyzer.core.history import load_safe_history, save_safe_history


def test_history_contains_only_safe_metadata(tmp_path: Path):
    password = "SyntheticHistoryPassword123!"
    result = analyze_password(password)
    path = tmp_path / "history.json"
    save_safe_history(result.safe_dict(), path)
    text = path.read_text(encoding="utf-8")
    assert password not in text
    data = load_safe_history(path)
    assert len(data) == 1
    assert "score" in data[0]
    assert "classification" in data[0]
