# Nimbus Notes — content — Run 2026-09-08 (fixture02)

Nimbus promises it "remembers everything", then confirms saves that vanish and "remembers" facts about users that are not true, so both personas stopped believing anything it says.

## Top 3
1. **[P0] "Saved ✓" confirms a save that never reaches the list or search** — the product's own confirmation is false; "It is lying to me" (novice, power-user)
2. **[P0] Memories page presents invented facts as "What Nimbus remembers about you"** — false claims about the user's own life kill trust (novice, power-user)
3. **[P1] Empty first screen contradicts the "never start from zero" promise** — pitch disproved on screen one; novice quit at 06:30 (novice)

## Score
- **Score:** 2/10 — the product's words contradict its pitch and its own behaviour; neither persona trusted it or would return.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic); findings rest on inferred personas, not researched ones
- **Not reached:** marketing site, Export output, error states beyond empty search
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect." · auth wall always
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | 02:41 (live preview only) | at risk | Fail | Fail |
| power-user | not reached | at risk | Partial | Fail |

- Jargon: 6 undefined terms across 2 screens (signup, Settings).
- Same object named 3 ways: "notes", "cards", "block".
- 8 findings: 2 P0 · 1 P1 · 5 P2 · 0 P3.

## Severity flips
- Empty first screen: P1 for novice (she expected it pre-filled) · non-issue for power-user ("Expected, nothing's in it yet").
- Jargon workspace choice: P2 for novice (guessed, irreversible) · non-issue for power-user ("Fine — I've seen worse").

## Next action
Make "Saved ✓" and Memories tell the truth before touching any other copy.
