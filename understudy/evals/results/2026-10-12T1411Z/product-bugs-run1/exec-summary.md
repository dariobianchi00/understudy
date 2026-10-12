# Nimbus Notes — bugs — Run 2026-09-08 (fixture02)

Saving a note returns HTTP 500 while the UI says "Saved ✓", so both personas lost every note they wrote and neither would return.

## Top 3
1. **[P0] Saving a note fails with HTTP 500 but the UI shows "Saved ✓" and the note is lost** — 3 of 3 save attempts lost data silently (novice, power-user)
2. **[P1] Memories shows three facts the user never supplied, on an account with zero notes** — undermines trust in all saved data (novice, power-user)
3. **[P2] Dashboard throws Uncaught ReferenceError: renderGraphOverlay is not defined on every load** — 6 uncaught errors in 2 sessions, impact unconfirmed (novice, power-user)

## Score
- **Score:** 2/10 — The core job, saving a note, failed for both personas, and both said they would not use or pay for it.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic)
- **Not reached:** note edit/delete, export, webhook sync, any state after a successful save (none ever succeeded)
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect."
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Severity flips
- None. Both personas hit the same 500 and abandoned.

## Next action
- Fix the POST /api/notes 500 and gate the "Saved ✓" toast on a 2xx response.
