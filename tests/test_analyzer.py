from password_strength_analyzer.core.analyzer import (
    analyze_password,
    character_diversity,
    entropy_estimate,
    has_keyboard_pattern,
    has_repeated_character,
    has_sequential_pattern,
    personal_overlap,
)


def test_common_password_is_detected():
    result = analyze_password("Password123!")
    assert result.common_password is True
    assert result.score < 65


def test_long_passphrase_scores_better_than_short_demo_password():
    weak = analyze_password("abc123")
    stronger = analyze_password("river-cactus-orbit-lantern-mango")
    assert stronger.score > weak.score


def test_character_diversity():
    result = character_diversity("Abc9!")
    assert result["uppercase"]
    assert result["lowercase"]
    assert result["digits"]
    assert result["symbols"]


def test_patterns():
    assert has_repeated_character("Hellooo")
    assert has_sequential_pattern("abc123")
    assert has_keyboard_pattern("qwerty")


def test_personal_context_is_detected():
    assert personal_overlap("student2026!", ["student", "college"])


def test_entropy_empty_is_zero():
    assert entropy_estimate("") == 0.0


def test_safe_result_does_not_contain_password():
    password = "SyntheticDemoPassword123!"
    result = analyze_password(password)
    safe = str(result.safe_dict())
    assert password not in safe
    assert "password" not in safe.lower() or "common_password" in safe.lower()
