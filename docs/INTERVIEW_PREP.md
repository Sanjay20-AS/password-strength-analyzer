# Interview Preparation

## 1. What problem does the project solve?

It gives users an explainable local assessment of password quality. Instead of only checking character types, it considers length, common passwords, dictionary terms, repeated characters, sequences, keyboard patterns, and optional context.

## 2. Why is `Password123!` weak even though it has many character types?

Because character diversity does not remove predictability. `Password` and common number/symbol suffixes are frequently used patterns.

## 3. Why not store the password?

A password is highly sensitive authentication material. Storing it creates unnecessary risk. The project uses ephemeral in-memory processing and stores only aggregate metadata when history is enabled.

## 4. What is entropy in this project?

It is an entropy-style mathematical estimate based on length and an estimated character pool. It assumes random selection, which is often false for human-created passwords, so it is only one signal.

## 5. What are false positives?

A detector may flag a word or pattern that is not necessarily dangerous in every context. That is why the application presents findings as signals and recommendations rather than absolute proof of insecurity.

## 6. How would you improve it for production?

I would add a stronger probabilistic password model, configurable organizational policies, privacy-preserving breached-password checks, secure deployment controls, observability that excludes secrets, CI security tests, and accessibility improvements.

## 7. What cybersecurity principles are demonstrated?

- Data minimization
- Least exposure of sensitive data
- Secure-by-design input handling
- Defensive security analysis
- Explainability
- Automated security regression testing
- Security awareness

## 8. What did you deliberately not build?

Password cracking, credential stuffing, login brute forcing, credential harvesting, and external credential collection were deliberately excluded because they are unnecessary for the defensive educational objective.
