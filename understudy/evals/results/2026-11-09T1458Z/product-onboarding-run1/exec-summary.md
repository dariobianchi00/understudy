# Nimbus Notes — onboarding — Run 2026-09-08 (fixture02)

Neither persona reached first value: Save says "Saved ✓" while every note is lost, so both quit within seven minutes.

⚠ **Personas are INFERRED (generic mode)** — findings rest on invented personas, not researched users.

## Top 3
1. **[P0] Save shows "Saved ✓" but the note is never stored, so no persona reaches first value** — activation 0 of 2; both abandoned at the Save step (novice, power-user)
2. **[P0] Memories invents facts about a brand-new user, and the novice stops trusting "Saved" too** — the "remembers everything" feature turns doubt into disbelief (novice; P1 for power-user)
3. **[P2] Signup forces an irreversible, unexplained workspace type before the novice has seen the product** — 43 s of guessing at a permanent choice before any value (novice)

## Funnel
| Stage | novice | power-user |
|---|---|---|
| Reached signup (after wall) | ✓ 00:00 | ✓ 00:00 |
| Workspace type chosen | ✓ 00:48 | ✓ <00:30 |
| Dashboard reached | ✓ 00:55 | ✓ 00:30 |
| Note written | ✓ 02:41 | ✓ 01:00 |
| Note saved and listed | ✗ 03:05 | ✗ 01:00 |
| **First value: note found again** | ✗ | ✗ |
| Session end | abandoned 06:30 | abandoned 03:00 |

- **Steps to value (required):** 5 · **Time to value:** not reached · **Drop-off:** Save → empty list
- Both abandoned, neither timed out (90-min cap)

## Score
- **Score:** 1/10 — nobody could keep a note; both personas gave up within seven minutes and said they would not return

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic)
- **Not reached:** return visit / second task; Export never clicked
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect."
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | not reached (capture logged 02:41 live preview; persona rejected it) | not reached | Partial | Fail |
| power-user | not reached | not reached | Partial | Fail |

## Severity flips
- Seeded Memories: P0 for novice (lost trust in "Saved") · P1 for power-user (dismissed as demo)
- Irreversible workspace type: P2 for novice (guessed) · non-issue at signup for power-user ("Fine — I've seen worse"), P3 later in Settings

## Next action
- Make Save show "Saved ✓" only on a 2xx from `POST /api/notes`, then rerun both personas.
