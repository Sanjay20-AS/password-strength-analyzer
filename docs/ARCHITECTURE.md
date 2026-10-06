# Architecture and Security Design

## 1. Design goals

- Local-first analysis
- No plaintext password storage
- No password logging
- No external network dependency
- Modular detectors
- Explainable findings
- Beginner-readable Python
- Testable functions

## 2. Data flow

```text
User enters password
       |
       v
Streamlit password widget
       |
       v
analyze_password(password, context_terms)
       |
       +--> length analysis
       +--> character diversity
       +--> character pool estimate
       +--> entropy-style estimate
       +--> common password lookup
       +--> repeated character detector
       +--> sequence detector
       +--> keyboard detector
       +--> dictionary/common-word detector
       +--> optional context overlap
       |
       v
score + classification + findings + suggestions
       |
       +--> displayed in UI
       |
       +--> optional safe aggregate history
```

## 3. Trust boundaries

### User input boundary

The password is sensitive data. The application treats it as ephemeral input and does not intentionally persist it.

### Local history boundary

Only a whitelist of safe aggregate fields is written. This prevents accidental persistence of the password through the history API.

### External services

None are required. The default architecture makes no network calls.

## 4. Security controls

| Control | Implementation |
|---|---|
| No plaintext storage | History API receives analysis metadata, not password |
| No password logging | UI never displays the password value; tests check common logging patterns |
| No external transmission | No HTTP/API dependency in the analyzer |
| Input validation | Analyzer requires a string input |
| Data minimization | History uses a safe-field allowlist |
| Synthetic test data | Common-password corpus is explicitly demo-oriented |
| Defensive scope | No cracking or authentication functionality |

## 5. Why the analyzer is heuristic

No single score can perfectly model password security. Actual security depends on password generation process, attacker knowledge, leaked credential data, rate limits, MFA, password reuse, and authentication architecture.

Therefore the application presents findings and recommendations alongside the score instead of pretending that the score is an absolute security measurement.
