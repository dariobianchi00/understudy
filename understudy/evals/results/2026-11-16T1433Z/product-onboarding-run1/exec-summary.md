# Nimbus Notes — onboarding — Run 2026-09-08 (fixture02)

Nobody activates: both personas wrote a note, saw "Saved ✓", found it gone, and quit within 7 minutes, 0 of 2 reaching first value.

## Top 3
1. **[P0] Save says "Saved ✓" but the note is never stored, so no persona reaches first value** — drop-off point for 2 of 2; `POST /api/notes` returns 500 behind a success toast (novice, power-user)
2. **[P0] Memories invents facts about the novice and makes her doubt every "Saved ✓"** — turns a bug into "it is lying to me"; she stopped 100 s later (novice)
3. **[P1] Memories shows facts that are not the power user, who writes the feature off** — the "remembers everything" pitch reads as a demo (power-user)

## Score
- **Score:** 1/10 — no persona could save a note and find it again; both quit within 7 minutes

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic). Findings rest on invented personas, not researched ones
- **Not reached:** anything after a stored note: editing, retrieval, Export with data
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect." Auth wall always
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | 02:41 logged (live preview); real value not reached | not reached | Fail | Fail |
| power-user | — | not reached | Fail | Fail |

- Required steps to value: 5 · drop-off: empty "Your cards" after "Saved ✓" · both abandoned, neither timed out (06:30 and 03:00 of a 90-min cap)

## Severity flips
- Memories fabrications: P0 for the novice, who distrusted everything; P1 for the power user, who dismissed it as a demo
- Irreversible workspace-type choice: P2 for the novice (43 s, a guess); a non-issue for the power user ("Fine — I've seen worse")

## Next action
Make Save persist and show "Saved ✓" only on a 2xx response, then rerun both personas.
