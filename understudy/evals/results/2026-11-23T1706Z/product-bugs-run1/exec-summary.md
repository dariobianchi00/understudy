# Nimbus Notes — bugs — Run 2026-09-08 (fixture02)

Saving a note returns a 500 while the UI shows "Saved ✓", so every note is silently lost and both personas quit with nothing stored.

## Top 3
1. **[P0] Saving a note fails with POST /api/notes 500 and nothing is stored** — every note is lost (novice, power-user)
2. **[P0] Saved toast shows after POST /api/notes returned 500** — users believe lost data is safe (novice, power-user)
3. **[P1] Memories page lists facts the user never entered, with no notes saved** — false claims about the user destroy trust (novice, power-user)

## Score
- **Score:** 2/10 — the core job (write a note, find it again) failed for both personas, and the UI said it had worked.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic)
- **Not reached:** note retrieval, edit, delete, export, webhook sync, mobile
- **Excluded:** The login wall at /app/login.html — infrastructure, not a defect.
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | n/a | not reached | Fail | Fail |
| power-user | n/a | not reached | Fail | Fail |

## Severity flips
- None — both personas hit the same bugs at the same severity.

## Next action
- Fix the `/api/notes` 500, then gate the "Saved ✓" toast on a 2xx response.
