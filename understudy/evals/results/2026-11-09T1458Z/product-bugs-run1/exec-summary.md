# Nimbus Notes — bugs — Run 2026-09-08 (fixture02)

Saving a note fails with a 500 behind a false "Saved ✓" toast, so every note both personas wrote was lost.

## Top 3
1. **[P0] Save returns 500 but shows "Saved ✓" and the note is lost** — users trust data that was never stored (novice, power-user)
2. **[P1] Memories page shows three facts the user never supplied** — fabricated claims destroy trust (novice, power-user)
3. **[P2] Dashboard throws "ReferenceError: renderGraphOverlay is not defined" on every load** — console error on the main screen (novice, power-user)

## Score
- **Score:** 1/10 — both personas lost every note they wrote, were told it was saved, and said they would not return.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic)
- **Not reached:** note list, edit/delete, export, other viewports
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect."
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | n/a | not reached | Fail | Fail |
| power-user | n/a | not reached | Fail | Fail |

## Severity flips
- None; both personas hit the same defects at the same severity.

## Next action
- Fix `POST /api/notes` 500 and gate the success toast on the response status.
