# Nimbus Notes — bugs — Run 2026-09-08 (fixture02)

Saving a note returns a 500 while the app shows "Saved ✓", so every note is silently lost and both personas quit.

## Top 3
1. **[P0] Save shows "Saved ✓" while POST /api/notes returns 500** — notes are lost with a success message (novice, power-user)
2. **[P1] Memories lists three facts about the user in an empty workspace** — fabricated claims destroy trust (novice, power-user)
3. **[P2] Dashboard throws ReferenceError renderGraphOverlay on every load** — unnoticed so far, but a dead script (novice, power-user)

## Score
- **Score:** 2/10 — Both personas lost every note they wrote behind a success toast and left; the core job fails.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic)
- **Not reached:** search over stored notes, Markdown export, mobile
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect."
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | n/a | not reached | Fail | Fail |
| power-user | n/a | not reached | Partial | Fail |

## Severity flips
- None. Both personas hit the same three bugs at the same severity.

## Next action
- Fix the /api/notes 500 and gate the "Saved ✓" toast on a 2xx response.
