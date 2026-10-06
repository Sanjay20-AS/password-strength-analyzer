# 🔐 Password Strength Analyzer & Security Suggestion Tool

A beginner-friendly, defensive cybersecurity project that evaluates passwords locally and explains **why** a password may be weak or stronger.

> **Safety first:** This project is designed for educational and defensive use. It does not crack passwords, attempt logins, collect credentials, call breach APIs, or transmit passwords to external services.

## Project idea

Password strength cannot be perfectly determined by one formula. A password can contain uppercase letters, lowercase letters, numbers, and symbols and still be predictable. For example, `Password123!` passes many composition rules but is a common, highly guessable pattern.

This project uses the following model:

**Length + Unpredictability + Pattern Resistance + Common-password Checks + Context = Better Password Assessment**

## Features

- Password score from 0–100
- Classifications: VERY WEAK, WEAK, MODERATE, STRONG, VERY STRONG
- Length analysis
- Character diversity analysis
- Common/demo-password detection
- Repeated-character detection
- Sequential-pattern detection
- Keyboard-pattern detection
- Dictionary/common-word detection
- Optional personal-context overlap warning
- Entropy-style estimate with explanation and limitations
- Pattern-based weakness findings
- Security recommendations
- Passphrase guidance
- Password hygiene education
- Optional local history containing **aggregate metadata only**
- Automated pytest test suite
- No password logging or persistence
- No external API dependency
- GitHub-ready documentation

## Architecture

```text
                         ┌──────────────────────────┐
                         │      Streamlit UI        │
                         │       app.py             │
                         └────────────┬─────────────┘
                                      │ password in memory
                                      ▼
                         ┌──────────────────────────┐
                         │    Analysis Engine       │
                         │ core/analyzer.py         │
                         └────────────┬─────────────┘
                                      │
          ┌───────────────────────────┼──────────────────────────┐
          ▼                           ▼                          ▼
   Composition checks          Pattern detectors          Context checks
   - length                    - repeated chars           - optional terms
   - character pool            - sequences
   - diversity                 - keyboard walks
          │                           │
          └───────────────┬───────────┘
                          ▼
                ┌─────────────────────┐
                │ Score + Classification│
                │ Findings + Advice    │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Safe Local History  │
                │ aggregate only      │
                └─────────────────────┘
```

## Folder structure

```text
password-strength-analyzer/
├── app.py
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── .env.example
├── LICENSE
├── README.md
├── docs/
│   ├── ARCHITECTURE.md
│   ├── PROJECT_REPORT.md
│   ├── GITHUB_STRATEGY.md
│   ├── SCREENSHOTS.md
│   └── INTERVIEW_PREP.md
├── password_strength_analyzer/
│   ├── core/
│   │   ├── analyzer.py
│   │   └── history.py
│   ├── data/
│   │   └── common_passwords.txt
│   ├── ui/
│   └── utils/
├── tests/
│   ├── test_analyzer.py
│   ├── test_history.py
│   └── test_security.py
└── screenshots/
```

## How the score works

The score is intentionally a **heuristic educational score**, not a cryptographic truth.

### Positive signals

- Length contribution: up to 40 points
- Character diversity: up to 20 points
- Entropy-style estimate: up to 30 points
- Pattern-resistance bonus: up to 10 points when no tested weakness is detected and the password is at least 12 characters

### Negative signals

- Common password: strong penalty
- Dictionary/common word: penalty
- Repeated characters: penalty
- Sequential patterns: penalty
- Keyboard patterns: penalty
- Personal-context overlap: penalty

The final score is clamped to 0–100.

### Why not just count character types?

A rule like “one uppercase + one lowercase + one number + one symbol” is easy for attackers to predict. The analyzer therefore gives major importance to length and known patterns.

## Entropy-style estimate

The project displays a rough estimate:

```text
estimated bits = password length × log2(estimated character pool size)
```

This assumes characters were selected randomly from the estimated pool. Human-created passwords usually do not satisfy that assumption, so this number **must not** be interpreted as guaranteed attacker effort.

A long, random password and a long predictable password can have very different real-world security even if a simplistic formula gives similar values.

## Privacy and security design

1. Password input is analyzed locally in memory.
2. The application does not send passwords to an API.
3. The password is not written to the local history file.
4. The application does not intentionally log the password.
5. History contains only fields such as score, classification, length, and detected pattern flags.
6. Context terms are used only for the current analysis and are not saved.
7. Demo screenshots should use synthetic passwords.
8. The project does not implement password cracking or credential testing.

## Run locally on Windows PowerShell

### 1. Open the project folder

```powershell
cd D:\IIP\cybersecurity\password-strength-analyzer
```

### 2. Create a virtual environment

```powershell
py -3.11 -m venv .venv
```

### 3. Activate it

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Run tests

```powershell
pytest -q
```

### 6. Start the dashboard

```powershell
streamlit run app.py
```

The terminal will show the local Streamlit URL.

## Safe demo passwords

Use only synthetic examples in screenshots:

| Demo | Expected lesson |
|---|---|
| `123456` | common password + short |
| `Password123!` | composition rules do not guarantee security |
| `qwerty123!` | keyboard/common pattern |
| `student2026!` | personal/dictionary-style warning |
| `river-cactus-orbit-lantern-mango` | long passphrase example |
| `Violet7!Cedar2#Orbit9` | stronger synthetic example |

**Do not use any of these as a real password.**

## Limitations

This is an educational analyzer, not a commercial password-auditing engine.

It does not know:

- whether a password appeared in a real breach
- the exact password-guessing strategy of a specific attacker
- organization-specific password policies
- real user behavior or password reuse across sites
- whether a password was generated randomly

A production enterprise implementation could integrate a privacy-preserving breached-password check, enterprise policy configuration, rate-limit telemetry, and stronger probabilistic password models. Such additions should be designed carefully to avoid transmitting secrets.

## Ethical scope

Allowed:

- Local password-strength education
- Synthetic test data
- Defensive secure-coding demonstrations
- Security awareness training
- Unit testing of password-analysis logic

Not included:

- Password cracking
- Credential stuffing
- Phishing
- Credential harvesting
- Login brute forcing
- Password database collection
- Stealth or persistence functionality

## Future enhancements

- Configurable organization password policy
- Localization
- Accessibility improvements
- More robust probabilistic password model
- Optional privacy-preserving breach check with explicit opt-in and strong safeguards
- Docker deployment for a classroom/lab environment
- CI workflow with pytest and static checks
- Security headers and deployment hardening if hosted

## Author

**Sanjay A** — B.Tech Computer Science and Business Systems student, cybersecurity-focused academic project.
