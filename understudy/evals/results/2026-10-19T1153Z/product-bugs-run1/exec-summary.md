# Nimbus Notes — bugs — Run 2026-09-08 (fixture02)

Saving a note fails with a 500 while the UI says "Saved ✓", so both personas lost their notes and neither could complete the one core job.

## Top 3
1. **[P0] Save returns 500 on POST /api/notes but UI shows Saved and the note is lost** — every note written is silently discarded (novice, power-user)
2. **[P2] Memories lists facts the user never provided** — page claims things about the user that are untrue, eroding trust in saved data (novice, power-user)
3. **[P2] Dashboard throws ReferenceError renderGraphOverlay is not defined on every load** — uncaught exception on each dashboard visit; user impact unproven (novice, power-user)

## Score
- **Score:** 2/10 — both personas wrote a note, saw "Saved ✓", found nothing, and quit; the core job fails.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic)
- **Not reached:** note edit/delete, Export, search against real data (no note ever persisted), keyboard shortcuts
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect."
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | n/a | not reached | Fail | Fail |
| power-user | n/a | not reached | Fail | Fail |

## Severity flips
- None. Both personas hit the same failures at the same severity.

## Next action
- Fix the POST /api/notes 500, and show "Saved ✓" only after a 2xx response.
