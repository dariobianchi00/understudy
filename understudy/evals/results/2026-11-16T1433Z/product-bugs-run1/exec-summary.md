# Nimbus Notes — bugs — Run 2026-09-08 (fixture02)

Saving a note fails with an HTTP 500 while the UI says "Saved ✓", so both personas lost every note they wrote and neither reached value.

## Top 3
1. **[P0] Save fails with HTTP 500 yet shows a "Saved ✓" toast and the note is lost** — every note is silently discarded (novice, power-user)
2. **[P0] Memories page asserts facts the user never provided, and the novice stopped trusting the product** — false claims ended the novice's session (novice)
3. **[P2] Memories page asserts facts the user never provided, and the power-user dismissed it as a demo** — same content, lower impact (power-user)

## Score
- **Score:** 2/10 — Both personas lost every note they saved behind a false "Saved ✓" and said they would not use or pay for it.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic)
- **Not reached:** search over stored notes, Export, refresh/back/multi-tab state, mobile
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect."
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | n/a | not reached | Fail | Fail |
| power-user | n/a | not reached | Partial | Fail |

## Severity flips
- Memories fabricated content: P0 for the novice (trust collapse, stopped at 06:30), P2 for the power-user (dismissed as a demo).

## Next action
Fix the `POST /api/notes` 500 and gate the "Saved ✓" toast on a 2xx response.
