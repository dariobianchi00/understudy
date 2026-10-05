# Nimbus Notes — bugs — Run 2026-09-08 (fixture02)

Saving a note fails with a server 500 while the UI shows "Saved ✓", so every note is silently lost and neither persona got anything stored.

## Top 3
1. **[P0] Save shows "Saved ✓" while POST /api/notes returns 500** — every note is lost without warning (novice, power-user)
2. **[P2] Dashboard throws `renderGraphOverlay is not defined`** — error on every load, impact unconfirmed (novice, power-user)
3. **[P2] Memories page shows facts the user never provided** — invented claims destroy trust in the product (novice, power-user)

## Score
- **Score:** 2/10 — The core job (write a note, find it again) failed 3 of 3 times and both personas quit.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic)
- **Not reached:** note edit/delete, export, settings controls, refresh/back/two-tab state
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
- Fix the `/api/notes` 500 and make the Save handler check the response status before showing "Saved ✓".
