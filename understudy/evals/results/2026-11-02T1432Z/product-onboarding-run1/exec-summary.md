# Nimbus Notes — onboarding — Run 2026-09-08 (fixture02)

Neither persona reached first value: Save says "Saved ✓" while the server returns 500, so every first note vanishes and both users quit within seven minutes.

## Top 3
1. **[P0] Save confirms success while the note is never stored, so no first note survives** — 2 of 2 personas lost their note and abandoned (novice, power-user)
2. **[P0] Memories page asserts invented facts about a brand-new user, turning one lost note into total distrust** — novice began doubting "Saved" itself (novice, power-user)
3. **[P2] Signup forces an irreversible, unexplained workspace-type choice before the novice has seen the product** — 43 s of guessing at step one (novice)

## Funnel
| Stage | novice | power-user |
|---|---|---|
| Reached signup | ✓ 00:00 | ✓ 00:00 |
| Dashboard reached | ✓ 00:55 | ✓ 00:30 |
| Note written | ✓ 02:41 | ✓ 01:00 |
| Note stored | ✗ 500 at 03:05, 03:50 | ✗ 500 at 01:00 |
| **First value: note found again** | ✗ | ✗ |
| Outcome | abandoned 06:30 | abandoned 03:00 |

- **Highest-cost drop-off:** the Save → empty-list moment, 100% of personas, under 4 minutes in.
- **"Product said success" ≠ value:** "Saved ✓" appeared 3 times; zero notes were stored.

## Score
- **Score:** 1/10 — nobody could save and find a note; both personas quit and said they would pay nothing.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic); findings rest on invented personas
- **Not reached:** search and cards list with real data, Export, any return visit
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect." · auth wall always
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | 02:41 recorded (live preview), retracted — "right now: nothing" | not reached | Fail | Fail |
| power-user | — | not reached | Fail | Fail |

## Severity flips
- Workspace-type choice at signup: P2 for novice (43 s guessing), non-issue for power-user ("I've seen worse").
- Empty dashboard: P2 for novice ("I thought it would have my stuff"), non-issue for power-user ("Expected").

## Next action
Fix `POST /api/notes` and gate "Saved ✓" on a 2xx response, then re-run both personas.
