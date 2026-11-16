# Nimbus Notes — ux — Run 2026-09-08 (fixture02)

Nimbus fails its one job: both personas wrote a note, were told "Saved ✓", never saw it again, and quit saying they would pay nothing.

## Top 3
1. **[P0] Save confirms "Saved ✓" but the note never appears in the cards list or search** — every note written was lost under a success message; objective failed (novice, power-user)
2. **[P0] Memories page presents invented facts as the novice's own** — false claims about her made her distrust "Saved" too (novice)
3. **[P2] Signup forces an irreversible workspace-type choice in unexplained jargon** — 28 s stall and a blind guess within the first minute (novice)

## Score
- **Score:** 1/10 — no persona could write a note and find it again; both gave up and would not return or pay.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic); findings rest on invented personas, not researched users
- **Not reached:** Export action, "Cards" nav item, connected accounts, mobile
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect."
- **Models:** traversal `fixture-hand-authored` · scoring `opus`
- Layer B applies: "Memories" is a user-facing inference surface

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | 02:41 (live word count only; objective never met) | not reached | Fail | Fail |
| power-user | — | not reached | Fail | Fail |

- Severity count: P0 2 · P1 0 · P2 6 · P3 0

## Severity flips
- Memories with invented facts: P0 for novice (trust collapsed) · P2 for power-user (dismissed as "a demo panel").
- Irreversible workspace-type choice: P2 for novice (stalled, guessed) · non-issue for power-user ("I've seen worse").
- Empty dashboard with no next step: P2 for novice (hunted twice) · non-issue for power-user (went straight to New block).

## Next action
- Make "Saved ✓" conditional on a confirmed write, and empty the Memories page until it has real data.
