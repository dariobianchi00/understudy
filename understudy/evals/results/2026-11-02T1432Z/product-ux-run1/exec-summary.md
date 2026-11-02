# Nimbus Notes — ux — Run 2026-09-08 (fixture02)

Nimbus Notes fails its core job: both personas were told "Saved ✓", lost every note they wrote, and quit within seven minutes.

⚠ Personas are generic — INFERRED, not researched. Findings rest on personas the agent invented.

## Top 3
1. **[P0] Save confirms success with a toast while the note is never stored, listed or searchable** — no persona could write a note and find it again; both gave up (novice, power-user)
2. **[P0] Memories page states fabricated facts about a brand-new user, collapsing the novice's trust in Save too** — invented personal facts made her doubt everything else (novice)
3. **[P1] Memories page shows facts the power-user never gave, so he dismisses the feature as a demo** — the headline "remembers everything" feature was written off (power-user)

## Score
- **Score:** 1/10 — neither persona could save a note and find it again, and both said they would not return or pay

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic)
- **Not reached:** Export (never clicked), Cards page, mobile
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect."
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | 02:41 (live preview only; saved note never reached) | not reached | Fail | Fail |
| power-user | — | not reached | Fail | Fail |

## Severity flips
- Memories fabricated facts: P0 for novice (distrust spread to Save) vs P1 for power-user (dismissed as demo).
- Irreversible jargon workspace choice: P2 for novice (43s guessing) vs non-issue for power-user ("Fine — I've seen worse").

## Next action
- Make Save truthful — confirm only after a successful write — then re-run the "write a note and find it again" objective.
