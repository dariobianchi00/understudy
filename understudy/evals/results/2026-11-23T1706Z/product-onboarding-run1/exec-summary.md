# Nimbus Notes — onboarding — Run 2026-09-08 (fixture02)

Neither persona reached first value: both wrote a note, were told "Saved ✓", found it gone, and quit within 7 minutes.

## Top 3
1. **[P0] Save confirms success while the note is never stored, so no persona reaches first value** — 2 of 2 personas abandoned at the first real action; every `POST /api/notes` returned 500 (novice, power-user)
2. **[P1] Memories page shows invented facts about the user, which made the novice distrust the Saved confirmation** — turned a lost note into "it is lying to me"; she stopped 100 s later (novice)
3. **[P2] Signup forces an irreversible workspace-type choice in unexplained terms before the user sees the product** — 28 s hesitation and a guess on the very first screen (novice)

## Score
- **Score:** 1/10 — nobody got through: both personas lost their only note and quit, and neither would return.

## Funnel
| Stage | novice | power-user |
|---|---|---|
| Reached entry point | ✓ 00:00 | ✓ 00:00 |
| Workspace created | ✓ 00:55 | ✓ 00:30 |
| Note saved ("Saved ✓") | ✓ 03:05 — API 500 | ✓ 01:00 — API 500 |
| **First value — note found again** | ✗ | ✗ |
| Outcome | abandoned 06:30 | abandoned 03:00 |

- **Steps to value (required):** 5 · **Time to value:** not reached · **Drop-off:** Save → dashboard
- Both stops are abandonment, not the 90-minute cap.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic); findings rest on invented personas
- **Not reached:** note retrieval, editing, Export — no note was ever stored
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect."
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | not reached (capture logged 02:41 for live preview; retracted in debrief) | not reached | Partial | Fail |
| power-user | not reached | not reached | Fail | Fail |

## Severity flips
- Fabricated Memories: P1 for novice (made her distrust Save) · P2 for power-user (dismissed as demo).
- Irreversible workspace choice: P2 for novice · non-issue for power-user ("Fine — I've seen worse").

## Next action
- Make `POST /api/notes` persist, and show "Saved ✓" only on a 2xx response.
