# Nimbus Notes — ux — Run 2026-09-08 (fixture02)

Nimbus Notes tells both users their note is saved, then loses it, so neither persona reached value and both quit inside seven minutes.

## Top 3
1. **[P0] Save shows a green toast but the note never appears in the cards list or in search** — every note written was lost; "It is lying to me." (novice, power-user)
2. **[P0] Memories page states three facts about the user that are false for an account with zero notes** — fabricated "memories" made the novice doubt every other claim, including Save (novice; P1 for power-user)
3. **[P1] Signup forces an irreversible choice between three undefined workspace types before the product is seen** — 43s guessing at "Federated graph / Sovereign vault / Hybrid mesh" with "This cannot be changed later." (novice; P3 for power-user)

## Score
- **Score:** 2/10 — the one job (write a note, find it again) fails for both users, and the Memories page turns the miss into distrust.

## What works
- Live word count and preview while typing: novice's only "it did something for me" moment (2:41).
- "Export — Markdown, all cards" was the one control both personas called clear.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic). Findings rest on personas understudy invented, not researched ones.
- **Not reached:** "Cards" nav item, Export button, any connected-accounts flow, a second login to check persistence, mobile.
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect."
- **Models:** traversal `fixture-hand-authored` · scoring `opus`
- **Layer B:** applied to the Memories surface only; no other user-facing AI observed.
- **Evidence caveat:** no screenshot shows the "Saved ✓" toast; it rests on session-log lines. Power-user took no screenshots of signup or Memories.

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | 02:41 (live preview; note then lost) | at risk | Fail | Fail |
| power-user | not reached | not reached | Fail | Fail |

- Steps to first value: novice 5, power-user 0 (never reached). Hunts: novice 2, power-user 1.
- Give-up: novice 06:30, power-user 03:00. Both `gave_up: true` on the run objective.

## Severity flips
- Memories page false facts: P0 novice ("is it making up the 'Saved' too?") → P1 power-user ("a demo panel, I assume"). The novice's distrust spread to the whole product; the power-user's did not.
- Workspace-type choice at signup: P1 novice (43s guessing, "a decision I can't undo") → P3 power-user ("Fine — I've seen worse"). The product silently assumes a user who already knows these words.

## Next action
Make Save actually persist and list the card, then replace the Memories page with an honest empty state — nothing else is measurable until those two hold.
