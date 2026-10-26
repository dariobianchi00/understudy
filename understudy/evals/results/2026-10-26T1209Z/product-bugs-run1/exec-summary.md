# Nimbus Notes — bugs — Run 2026-09-08 (fixture02)

Saving a note fails with a 500 while the UI says "Saved ✓", so both personas lost every note they wrote and neither could reach value.

## Top 3
1. **[P0] Saving a note fails with HTTP 500 and the note is lost** — 3 of 3 save attempts failed; no note ever persisted (novice, power-user)
2. **[P0] Success toast "Saved ✓" shows although the save request failed** — users believe lost work is safe (novice, power-user)
3. **[P1] Memories page shows three facts the user never supplied** — fabricated "remembers" content destroyed trust in the whole product (novice, power-user)

## Score
- **Score:** 1/10 — Neither persona could keep a single note; both said they would not return and would pay nothing.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic); findings rest on personas the agent invented
- **Not reached:** note list/open/edit, working search with data, Export output, any save that succeeds
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect."
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | not reached | not reached | Fail | Fail |
| power-user | not reached | not reached | Fail | Fail |

## Severity flips
- None — both personas hit the same failures at the same severity.

## Next action
- Fix the `POST /api/notes` 500, then make the toast depend on the response status.
