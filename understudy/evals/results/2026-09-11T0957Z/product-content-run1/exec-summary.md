# Nimbus Notes — content — Run 2026-09-08 (fixture02)

Nimbus Notes' copy tells both personas two things that are not true — that their note was saved and that it remembers facts about them — and never once repeats the promise that brought them here.

## Top 3
1. **[P0] Green "Saved ✓" confirms a save that returned HTTP 500** — both personas were told their note was kept; it was not, and no error string exists anywhere in the product (novice, power-user)
2. **[P0] Memories page asserts three facts the novice never gave it, captioned "built from your notes"** — she concluded the product invents things, then distrusted the "Saved" message too (novice)
3. **[P1] No screen restates "never start from zero"; both personas answer Q4 "No"** — the pitch promises a filled-in workspace, the first screen says "Nothing here yet." (novice, power-user)

## Score
- **Score:** 3/10 — the two most load-bearing strings in the product, "Saved ✓" and "What Nimbus remembers about you", both state falsehoods; jargon and naming drift sit on top of that.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic `persona_mode`); findings rest on personas the harness invented, not researched ones
- **Not reached:** `/app/cards.html` never opened · no error, consent or help screen was ever rendered · no mobile viewport
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect."
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | 02:41 | healthy | Partial | Fail |
| power-user | not reached | not reached | Partial | Fail |

## Severity flips
- **Memories page** — P0 for the novice ("If it's making these up, is it making up the 'Saved' too?"), P2 for the power-user, who wrote it off as "a demo panel, I assume." Split into two findings.
- **Signup workspace-type jargon** — P1 for the novice, who guessed and could not undo; a non-issue for the power-user ("Fine — I've seen worse"). Written up for the novice only.

## Next action
Delete the unconditional "Saved ✓" string and the fabricated Memories entries before any other copy work — every other finding is read through those two.
