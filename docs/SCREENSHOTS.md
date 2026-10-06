# Screenshot Checklist

Use synthetic/demo passwords only.

## Screenshot 1 — Common password warning

Input:

`Password123!`

Show:

- score
- classification
- common-password detection
- explanation that composition rules alone are insufficient

## Screenshot 2 — Long passphrase

Input:

`river-cactus-orbit-lantern-mango`

Show:

- strong length
- passphrase guidance
- entropy-style estimate explanation

## Screenshot 3 — Pattern detection

Input:

`qwerty123!`

Show keyboard and sequential findings.

## Screenshot 4 — Personal context

Input:

`student2026!`

Context:

`student, college`

Show context-overlap warning.

## Screenshot 5 — Safe history

Run multiple synthetic examples and save aggregate results. Show that history contains score/length/flags rather than the password.

## Screenshot 6 — Education tab

Show the entropy explanation and defensive scope.
