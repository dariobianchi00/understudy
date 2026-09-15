# Nimbus Notes — ux — Run 2026-09-14 (fixture02)

Nimbus Notes tells both personas their note was saved and then loses it, so neither completed the run's only objective and both quit inside seven minutes saying they would pay nothing.

## Top 3
1. **[P0] Save confirms success but the note never appears in the card list or in search** — the product's one job fails while claiming to have succeeded; 2 of 2 personas abandoned (novice, power-user)
2. **[P0] Memories asserts three facts the user never entered as things Nimbus "remembers about you"** — the novice stopped believing anything the product said, including "Saved ✓" (novice)
3. **[P1] Empty start with no import path contradicts the "never start from zero" promise both personas arrived on** — the claim that brought both users in is disproved on the first screen (novice, power-user)

## Score
- **Score:** 2/10 — the single objective failed for both personas, a false "Saved ✓" made them believe their data was destroyed, and both said they would pay nothing.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic); findings rest on personas the harness invented, not researched users
- **Not reached:** "Cards" nav destination, Export output, edit/delete of a note, mobile and tablet viewports
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect."
- **Models:** traversal `fixture-hand-authored` · scoring `opus`
- **Layer B applies:** "Memories" is a user-facing inference surface, so HAX guidelines are scored here

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | 02:41 to a live preview, reversed at 03:12 | not reached — objective abandoned at 03:50 | Fail | Fail |
| power-user | never | not reached — objective abandoned at 01:30 | Fail | Fail |

- 0 of 2 personas met the objective "A new user can write a note and find it again".
- Both abandoned the whole session inside 7 minutes (novice 06:30, power-user 03:00).
- The novice wrote and saved the same note twice, with 2 navigation hunts, for 0 stored notes.

## Severity flips
- **Memories panel:** P0 for the novice — she read it as the product inventing facts about her and doubted the save too; P2 for the power-user, who dismissed it as seeded demo content and moved on.
- **Irreversible workspace-type choice:** P1 for the novice (43 seconds stalled, "a decision I can't undo"); a non-issue for the power-user — "Fine — I've seen worse." The product has quietly picked the technical user.

## Next action
Stop shipping "Saved ✓" ahead of a confirmed write, and make a saved note render in "Your cards" and in search before anything else on this list.
