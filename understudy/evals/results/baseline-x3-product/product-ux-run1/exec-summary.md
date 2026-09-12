# Nimbus Notes — ux — Run 2026-09-08 (fixture02)

Nimbus tells both personas "Saved ✓" and then loses every note they write, so neither could complete the one job it exists for, and both quit inside seven minutes with zero trust left.

## Top 3
1. **[P0] Save shows "Saved ✓" then the note is absent from the list and from search** — every note written this run was lost behind a success toast; both personas gave up on it (novice, power-user)
2. **[P0] Memories page states facts about the user that the user never gave it** — three false "memories" after one note; the novice concluded the product fabricates and named it her quit point (novice; P1 for power-user)
3. **[P1] Irreversible workspace type demanded in three undefined terms before any value is shown** — 43 seconds stalled on an un-undoable choice in the first minute (novice; P3 for power-user)

## Score
- **Score:** 2/10 — the core write-and-find job fails for both personas behind a false success message, and the one "smart" surface shows invented facts.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic); findings rest on personas the run invented, not researched users
- **Not reached:** "Cards" nav item, Export, note detail/edit/delete, non-empty search, mobile
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect." — auth wall never scored
- **Models:** traversal `fixture-hand-authored` · scoring `opus`
- **Layer B:** applied to the Memories surface only; no other AI surface observed
- **Capture gap:** `04-note-saved-toast.png` shows the empty form, not the toast; "Saved ✓" wording rests on session logs

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | 02:41 (live preview only; no note ever persisted) | at risk | Partial — "supposed to keep my notes … right now: nothing"; names 2 of 3 | Fail |
| power-user | not reached | not reached | Partial — "accepts a note and then loses it"; names 2 of 3, one broken | Fail |

- Steps to first value: novice 5 · power-user 0 (never reached)
- Hunts: novice 2 · power-user 1
- Quit: novice 06:30 · power-user 03:00 — both with the objective failed

## Severity flips
- Memories with invented facts: **P0 novice** ("is it making up the Saved too?") vs **P1 power-user** ("a demo panel, I assume") — the product reads as a liar to a newcomer and as a demo to an expert.
- Workspace-type screen: **P1 novice** (43 s stalled, "a decision I can't undo") vs **P3 power-user** ("Fine — I've seen worse") — the screen assumes a user who already knows the terms.
- Keyboard shortcuts: power-user P2 only; the novice never tried, so not a flip.

## Next action
Make `/app/new.html` show "Saved ✓" only on a successful save and surface the failure otherwise — nothing else in this report matters until a note persists.
