# Nimbus Notes — onboarding — Run 2026-09-08 (fixture02)

No persona reached first value: Nimbus shows "Saved ✓" while every save returns a 500, so both personas' first note vanished and both quit within seven minutes.

## Top 3
1. **[P0] Save shows "Saved ✓" while POST /api/notes returns 500, so no first note ever persists** — 0 of 2 personas activated; the funnel stops at its first real task (novice, power-user)
2. **[P1] Memories page asserts invented facts about a brand-new user, making the novice doubt every save** — turned a lost note into "It is lying to me"; novice would stop at 06:30 (novice)
3. **[P2] Signup forces an irreversible, unexplained workspace-type choice before the user has seen the product** — 43 s of guessing at step 1; novice picked "Hybrid mesh" blind (novice)

## Score
- **Score:** 1/10 — neither persona kept a single note; both gave up and said they would pay nothing

## Funnel

| Stage | novice | power-user |
|---|---|---|
| Reached entry point (after auth wall) | ✓ 00:00 | ✓ 00:00 |
| Workspace type chosen | ✓ 00:48 (guessed) | ✓ ~00:30 |
| Dashboard reached | ✓ 00:55 | ✓ 00:30 |
| First note written | ✓ 02:41 | ✓ 01:00 |
| Note saved and visible in list | ✗ 03:12 (retried 03:50, failed again) | ✗ 01:00 |
| Note found by search | ✗ 03:30 | ✗ 01:00 |
| **First value reached** | ✗ | ✗ |
| Stopped | abandoned 06:30 — "I'd stop here" | abandoned 03:00 — "Enough." |

**Steps to value (required path):** 5 · **Time to value:** not reached · **Drop-off:** Save → list/search, both personas

- Both are **abandonments, not time-outs**: 06:30 and 03:00 of a 90-minute cap.
- Required path is 5 steps (pick type → Create workspace → New block → type → Save); the path was short, it just ended in a failure.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic). Findings rest on personas the agent invented, not researched users.
- **Not reached:** anything after a persisted note — second task, editing, retrieval, export actually run
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect." Auth wall never scored.
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | not reached (capture logged 02:41 for the live preview; persona rejected it — Q1 "right now: nothing") | not reached | Fail | Fail |
| power-user | not reached | not reached | Fail | Fail |

## Severity flips
- Memories page with invented facts: **P1 for novice** (read it as proof the product lies) vs **P2 for power-user** (dismissed as "a demo panel").
- Irreversible workspace-type choice: **P2 for novice** (43 s, blind guess) vs non-issue for power-user ("Fine — I've seen worse").

## Next action
Make Save fail loudly on a non-2xx response, fix the POST /api/notes 500, then re-run both personas.
