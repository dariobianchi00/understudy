# Nimbus Notes — ux — Run 2026-09-08 (fixture02)

Nimbus tells both personas "Saved ✓" on a note it never keeps and shows them memories that are not theirs, so a product whose whole promise is remembering was abandoned by 2 of 2 users inside 7 minutes with zero notes and zero trust.

## Top 3
1. **[P0] "Saved ✓" confirms a save that never happened; the note never appears in Cards or search** — every note either persona wrote was lost behind a success toast; both quit here (novice, power-user)
2. **[P0/P1] Memories page states three facts about the user that are not true** — the novice stopped believing any message the product shows; the power-user wrote the headline feature off as a demo (novice P0, power-user P1)
3. **[P1] Signup demands an irreversible choice between three undefined workspace types before showing the product** — the novice's first screen is a 43-second stall and a guess marked "cannot be changed later" (novice)

## Score
- **Score:** 2/10 — the one job (write a note, find it again) failed for both personas, the product said it succeeded, and the surface meant to prove "remembers everything" showed invented facts.

## What works
- Live word count and preview in the editor — the novice's first "it did something for me" at 2:41.
- "Export" · "Markdown, all cards" — the one control both personas understood without help.
- Two-item happy path (nav → New block → Save) is short; nothing about the layout itself slowed anyone.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic); findings rest on personas the run invented, not researched users
- **Not reached:** "Cards" nav item, Export output, any note detail view, mobile
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect."
- **Models:** traversal `fixture-hand-authored` · scoring `opus`
- **Layer B:** applied only to the Memories surface — the one place the product infers something about the user
- **Evidence gap:** the toast itself was never captured (`04-note-saved-toast.png` shows the blank editor); the P0 rests on session logs, post-save screenshots and both debriefs

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | 02:41 (live preview only; no note ever persisted) | at risk | Partial — "supposed to keep my notes… right now: nothing"; names 2 uses | Fail |
| power-user | not reached | not reached | Partial — "accepts a note and then loses it"; names 2 uses, one broken | Fail |

- Steps to first value: novice 5 · power-user 0 (never reached)
- Times had to hunt: novice 2 · power-user 1
- Give-up point: novice 03:50 (second failed save) · power-user 01:30 (first failed save + dead shortcuts)
- Objective "write a note and find it again": 0 of 2

## Severity flips
- **Memories page** — P0 for the novice ("is it making up the 'Saved' too?"), P1 for the power-user ("a demo panel, I assume"): the same fabricated content breaks trust in everything for one user and in one feature for the other.
- **Workspace-type gate** — P1 for the novice (43 s stalled, chose by guessing), non-issue for the power-user ("Fine — I've seen worse"): the product has silently picked a user who already knows what a federated graph is.
- **Keyboard shortcuts** — P2 for the power-user; the novice never tried, so no flip could be observed.

## Next action
Make "Saved ✓" mean saved — gate the toast on a confirmed write and show a real error otherwise — then empty the Memories page for new workspaces; nothing else in this report is testable until a note survives.
