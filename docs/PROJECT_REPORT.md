# Project Report

## Title

**Password Strength Analyzer & Security Suggestion Tool**

## Abstract

Passwords remain a common authentication weakness because users often choose short, reused, predictable, or personally meaningful credentials. A simple composition rule such as requiring uppercase letters, lowercase letters, numbers, and symbols does not reliably identify predictable passwords. This project presents a defensive, local password-strength analysis tool that combines length analysis, character diversity, common-password detection, dictionary checks, repeated-character detection, sequential-pattern detection, keyboard-pattern detection, optional personal-context analysis, and an entropy-style estimate. The system produces an explainable score, classification, weaknesses, and security recommendations. The application is designed with privacy in mind: passwords are processed locally in memory and are not stored, logged, or transmitted by default. Optional history contains only safe aggregate metadata.

## 1. Problem statement

Many password-strength meters overemphasize character composition. Users can therefore create credentials that technically satisfy complexity rules but remain easy to guess. A better educational tool should explain multiple dimensions of password quality.

## 2. Objectives

1. Analyze passwords locally.
2. Avoid storing or transmitting plaintext passwords.
3. Detect common and predictable patterns.
4. Provide an explainable score and classification.
5. Educate users about passphrases and password hygiene.
6. Provide automated tests for security-sensitive behavior.
7. Produce GitHub-ready proof of defensive cybersecurity work.

## 3. Functional requirements

- Password input
- Score generation
- Five strength classes
- Length analysis
- Character diversity analysis
- Common-password detection
- Repeated-character detection
- Sequential-pattern detection
- Keyboard-pattern detection
- Dictionary/common-word detection
- Optional context overlap
- Entropy-style estimate
- Findings and recommendations
- Passphrase guidance
- Safe aggregate history

## 4. Non-functional requirements

- Local-first
- Beginner-friendly
- Explainable
- Modular
- Testable
- No credential theft
- No password cracking
- No unnecessary network communication

## 5. Technology stack

- Python 3.11+
- Streamlit
- Pandas
- Pytest
- JSON for local aggregate history
- Git/GitHub

## 6. Modules

### Password analysis engine

Contains scoring, classification, character analysis, entropy-style calculation, and pattern detectors.

### Common-password checker

Uses a small synthetic/demo corpus. It is not intended to represent a real leaked-password database.

### Security recommendation engine

Converts findings into actionable guidance such as using longer passphrases, avoiding common patterns, and enabling MFA.

### Safe history module

Stores only aggregate metadata such as score, classification, length, entropy estimate, and boolean detector results.

### Dashboard

Streamlit provides the interactive user interface and educational content.

## 7. Algorithm overview

The score starts with positive signals from length, character diversity, and entropy-style estimate. It then subtracts penalties for known weaknesses. The result is clamped to 0–100 and mapped to a classification.

The approach is deliberately explainable rather than claiming to be a perfect model of real attacker behavior.

## 8. Security considerations

The password is a sensitive input. The application therefore avoids logging and persistence. The history module uses an allowlist of safe metadata fields. The project does not implement authentication attempts, credential testing, cracking, or external breach lookups.

## 9. Testing

Tests cover:

- common-password detection
- length/score comparison
- character diversity
- repeated characters
- sequential patterns
- keyboard patterns
- personal-context detection
- entropy behavior
- password exclusion from safe result metadata
- safe history persistence
- basic source-level password logging regression checks

## 10. Expected outcome

The final application provides an interactive cybersecurity dashboard that not only rates a password but explains why a password may be predictable and how users can improve their password hygiene.

## 11. Limitations

The tool is not a breach database, password-cracking engine, or enterprise password-policy service. Its entropy value is an estimate based on assumptions that human-generated passwords often violate.

## 12. Future scope

- More sophisticated probabilistic password modeling
- Configurable enterprise policies
- Privacy-preserving breach checking
- CI/CD security checks
- Dockerized deployment
- Accessibility and localization improvements

## 13. Conclusion

The project demonstrates practical defensive cybersecurity engineering by combining explainable password analysis with privacy-conscious implementation. It shows how secure design principles such as data minimization, local processing, modular detection, automated testing, and security education can be applied to a realistic security problem.
