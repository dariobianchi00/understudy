# Nimbus Notes — ux — Run 2026-09-08 (fixture02)

Nimbus Notes fails its one job: both personas wrote a note, were told "Saved ✓", and never saw it again, and both quit saying they would not return.

## Top 3
1. **[P0] Save shows "Saved ✓" but the note never reaches "Your cards" or search** — every note lost with a false success message; both gave up on the objective (novice, power-user)
2. **[P0] Memories page states invented facts about a brand-new novice, who then stopped trusting Saved** — "If it's making these up, is it making up the "Saved" too?" (novice)
3. **[P2] Signup forces an irreversible workspace type in unexplained terms before the product is shown** — novice guessed "Hybrid mesh" after 43 s at second 5 (novice)

## Score
- **Score:** 1/10 — neither persona could keep a single note; both said they would not return or pay anything.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic); findings rest on personas the agent invented, not researched users
- **Not reached:** Export never clicked; search never tested against a note that had actually saved; mobile
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect." Auth wall always excluded.
- **Models:** traversal `fixture-hand-authored` · scoring `opus`
- **Layer B applies:** "Memories" is a user-facing AI surface
- **Screenshots:** 3 of 13 do not show what their filename claims; those claims rest on session.log (see findings "Dropped")

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | 02:41 (live preview only; note never retained) | not reached | Fail | Fail |
| power-user | — | not reached | Fail | Fail |

- Objective "A new user can write a note and find it again": **failed 2/2**, `gave_up: true` for both
- Give-up points: novice 06:30, power-user 03:00
- Findings: P0 2 · P1 0 · P2 6 · P3 0

## Severity flips
- Memories invented facts: **P0 for novice** (spread distrust to "Saved") vs **P2 for power-user** ("a demo panel, I assume") — the page assumes a user who knows it is sample data.
- Irreversible workspace type: **P2 for novice** (43 s guess) vs non-issue for power-user ("Fine — I've seen worse") — signup assumes a technical user.

## Next action
- Make "Saved ✓" appear only after a successful save, and show an error with Retry when it fails.
