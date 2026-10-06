from pathlib import Path


def test_no_obvious_password_logging_in_source():
    root = Path(__file__).resolve().parents[1]
    forbidden = ["print(password)", "logger.info(password)", "logging.info(password)", "st.write(password)"]
    source_files = list(root.rglob("*.py"))
    combined = "\n".join(p.read_text(encoding="utf-8") for p in source_files if "tests" not in p.parts)
    for pattern in forbidden:
        assert pattern not in combined
