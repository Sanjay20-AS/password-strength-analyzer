"""Defensive, local password analysis engine.

Important: this module never stores, prints, logs, or transmits the password.
It returns safe analysis metadata only.
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable


BASE_DIR = Path(__file__).resolve().parents[1]
COMMON_FILE = BASE_DIR / "data" / "common_passwords.txt"

SEQUENTIAL_RUNS = [
    "abcdefghijklmnopqrstuvwxyz",
    "zyxwvutsrqponmlkjihgfedcba",
    "0123456789",
    "9876543210",
]
KEYBOARD_ROWS = [
    "qwertyuiop",
    "asdfghjkl",
    "zxcvbnm",
    "1234567890",
]
LEET_MAP = str.maketrans({"@": "a", "4": "a", "3": "e", "1": "i", "!": "i", "0": "o", "$": "s", "5": "s", "7": "t"})


@dataclass(frozen=True)
class Finding:
    category: str
    severity: str
    message: str
    penalty: int = 0


@dataclass(frozen=True)
class AnalysisResult:
    score: int
    classification: str
    length: int
    length_score: int
    character_pool_size: int
    character_diversity: dict[str, bool]
    estimated_entropy_bits: float
    common_password: bool
    repeated_character: bool
    sequential_pattern: bool
    keyboard_pattern: bool
    dictionary_word: bool
    personal_information_overlap: bool
    findings: tuple[Finding, ...]
    suggestions: tuple[str, ...]

    def safe_dict(self) -> dict:
        """Return only aggregate metadata; never include the password."""
        data = asdict(self)
        data["findings"] = [asdict(item) for item in self.findings]
        data["suggestions"] = list(self.suggestions)
        return data


def load_common_passwords(path: Path = COMMON_FILE) -> set[str]:
    if not path.exists():
        return set()
    return {
        line.strip().lower()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }


def normalize_for_dictionary(value: str) -> str:
    return value.lower().translate(LEET_MAP)


def character_diversity(password: str) -> dict[str, bool]:
    return {
        "uppercase": any(c.isupper() for c in password),
        "lowercase": any(c.islower() for c in password),
        "digits": any(c.isdigit() for c in password),
        "symbols": any(not c.isalnum() for c in password),
        "spaces": any(c.isspace() for c in password),
    }


def character_pool_size(diversity: dict[str, bool]) -> int:
    pool = 0
    if diversity["lowercase"]:
        pool += 26
    if diversity["uppercase"]:
        pool += 26
    if diversity["digits"]:
        pool += 10
    if diversity["symbols"]:
        pool += 33
    return pool


def entropy_estimate(password: str, pool_size: int | None = None) -> float:
    """A rough composition-based entropy-style estimate, not true password entropy."""
    if not password:
        return 0.0
    pool = pool_size if pool_size is not None else character_pool_size(character_diversity(password))
    if pool <= 1:
        return 0.0
    return round(len(password) * math.log2(pool), 1)


def has_repeated_character(password: str, run_length: int = 3) -> bool:
    return bool(re.search(rf"(.)\1{{{run_length - 1},}}", password, flags=re.IGNORECASE))


def has_sequential_pattern(password: str, minimum: int = 3) -> bool:
    normalized = password.lower()
    for run in SEQUENTIAL_RUNS:
        for size in range(minimum, min(len(run), len(normalized)) + 1):
            for start in range(0, len(run) - size + 1):
                if run[start:start + size] in normalized:
                    return True
    return False


def has_keyboard_pattern(password: str, minimum: int = 3) -> bool:
    normalized = password.lower()
    for row in KEYBOARD_ROWS:
        for size in range(minimum, len(row) + 1):
            for start in range(0, len(row) - size + 1):
                token = row[start:start + size]
                if token in normalized or token[::-1] in normalized:
                    return True
    return False


def contains_dictionary_word(password: str, common_words: Iterable[str] | None = None) -> bool:
    words = set(common_words or load_common_passwords())
    normalized = normalize_for_dictionary(password)
    if normalized in words:
        return True
    # Detect common terms embedded in longer passwords, while avoiding one-character matches.
    return any(len(word) >= 4 and word in normalized for word in words)


def is_common_password(password: str, common_passwords: Iterable[str] | None = None) -> bool:
    common = set(common_passwords or load_common_passwords())
    normalized = password.lower()
    return normalized in common or normalize_for_dictionary(password) in {normalize_for_dictionary(x) for x in common}


def personal_overlap(password: str, context_terms: Iterable[str] | None) -> bool:
    if not context_terms:
        return False
    normalized = normalize_for_dictionary(password)
    safe_terms = [normalize_for_dictionary(t.strip()) for t in context_terms if t and len(t.strip()) >= 3]
    return any(term in normalized for term in safe_terms)


def classify(score: int) -> str:
    if score < 25:
        return "VERY WEAK"
    if score < 45:
        return "WEAK"
    if score < 65:
        return "MODERATE"
    if score < 85:
        return "STRONG"
    return "VERY STRONG"


def analyze_password(password: str, context_terms: Iterable[str] | None = None) -> AnalysisResult:
    """Analyze one password in memory and return defensive findings.

    The caller must not log the input. This function deliberately returns no
    password value and performs no network operation.
    """
    if not isinstance(password, str):
        raise TypeError("password must be a string")

    length = len(password)
    diversity = character_diversity(password)
    pool = character_pool_size(diversity)
    entropy = entropy_estimate(password, pool)
    common = is_common_password(password)
    repeated = has_repeated_character(password)
    sequential = has_sequential_pattern(password)
    keyboard = has_keyboard_pattern(password)
    dictionary = contains_dictionary_word(password)
    personal = personal_overlap(password, context_terms)

    findings: list[Finding] = []

    # Length: emphasize modern passphrase-friendly length without treating it as the only factor.
    length_score = min(40, max(0, round(length * 2.5)))
    if length < 8:
        findings.append(Finding("Length", "high", "Password is shorter than the recommended minimum of 8 characters.", 15))
    elif length < 12:
        findings.append(Finding("Length", "medium", "Consider using at least 12 characters for better resistance.", 7))
    elif length < 16:
        findings.append(Finding("Length", "low", "Good length; a longer passphrase can provide additional resilience.", 2))

    if common:
        findings.append(Finding("Common password", "critical", "This password matches a common/demo password pattern and should not be used.", 35))
    if repeated:
        findings.append(Finding("Repeated characters", "medium", "Repeated characters make the password easier to predict.", 8))
    if sequential:
        findings.append(Finding("Sequential pattern", "medium", "A sequence such as abc, 123, or a reverse sequence was detected.", 8))
    if keyboard:
        findings.append(Finding("Keyboard pattern", "medium", "A keyboard walk such as qwerty or asdf was detected.", 8))
    if dictionary:
        findings.append(Finding("Dictionary/common word", "high", "A common word or demo dictionary term appears in the password.", 10))
    if personal:
        findings.append(Finding("Personal context", "high", "The password overlaps with optional context supplied for this analysis.", 12))

    diversity_count = sum(diversity[k] for k in ("uppercase", "lowercase", "digits", "symbols"))
    diversity_score = diversity_count * 5
    entropy_score = min(30, round(entropy / 6.5))
    pattern_flags = common or repeated or sequential or keyboard or dictionary or personal
    pattern_resistance_bonus = 10 if not pattern_flags and length >= 12 else 0

    score = length_score + diversity_score + entropy_score + pattern_resistance_bonus
    score -= sum(f.penalty for f in findings)
    score = max(0, min(100, score))

    suggestions: list[str] = []
    if length < 12:
        suggestions.append("Prefer a password or passphrase of at least 12–16 characters.")
    if common or dictionary:
        suggestions.append("Avoid common passwords and predictable words, even with added numbers or symbols.")
    if repeated or sequential or keyboard:
        suggestions.append("Avoid repeated characters, obvious sequences, and keyboard walks.")
    if personal:
        suggestions.append("Avoid names, dates, college/company terms, or other personal context that others could know.")
    if diversity_count < 2 and length < 16:
        suggestions.append("For short passwords, mixing character types can help; length is still more important than forced complexity.")
    suggestions.append("For memorable credentials, use a long unique passphrase made from unrelated words.")
    suggestions.append("Use a password manager to generate and store unique passwords for each account.")
    suggestions.append("Enable multi-factor authentication wherever available.")

    # Remove duplicate suggestions while preserving order.
    suggestions = list(dict.fromkeys(suggestions))

    return AnalysisResult(
        score=score,
        classification=classify(score),
        length=length,
        length_score=length_score,
        character_pool_size=pool,
        character_diversity=diversity,
        estimated_entropy_bits=entropy,
        common_password=common,
        repeated_character=repeated,
        sequential_pattern=sequential,
        keyboard_pattern=keyboard,
        dictionary_word=dictionary,
        personal_information_overlap=personal,
        findings=tuple(findings),
        suggestions=tuple(suggestions),
    )
