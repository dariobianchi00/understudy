# Nimbus Notes — bugs — Run 2026-09-08 (fixture02)

Nimbus Notes cannot save a note: the API returns 500 on every save, the UI lies with a "Saved ✓" toast anyway, and a separate panel fabricates personal facts about the user.

## Top 3
1. **[P0] Save reports success while the API call fails and the note is never stored** — every note is silently lost while the UI claims it worked (novice, power-user)
2. **[P0] Memories panel presents fabricated facts as the user's own data** — invents specific personal claims neither persona entered, destroying trust (novice, power-user)
3. **[P2] Uncaught ReferenceError on every dashboard load: `renderGraphOverlay is not defined`** — console exception on every visit, no visible break yet (novice, power-user)

## Score
- **Score:** 2/10 — the one thing this product must do, keep a note, fails outright and lies about it to both personas.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic persona_mode)
- **Not reached:** the "find a note again" half of the stated objective — never reached because no note ever persisted
- **Excluded:** The login wall at /app/login.html — infrastructure, not a defect.
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Numbers
| Persona | Save attempts | API failures | Notes ever found again | Console errors |
|---|---|---|---|---|
| novice | 2 | 2/2 (500) | 0 | 3× ReferenceError |
| power-user | 1 | 1/1 (500) | 0 | 2× ReferenceError |

## Severity flips
None — both personas hit identical severities on both P0 findings; the save failure and fabricated Memories content block novice and power-user equally.

## Next action
Fix the `/api/notes` 500 and stop showing a success toast on failure before anything else on this product is worth evaluating.
