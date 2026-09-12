# Nimbus Notes — content — Run 2026-09-08 (fixture02)

Nimbus promises to "remember everything" and then tells both personas, in its own words, that it saved a note it lost and remembers a life that is not theirs.

## Top 3
1. **[P0] "Saved ✓" confirms a save the server rejected, and no error copy exists** — both personas called it lying and quit; 0 notes kept across 3 attempts (novice, power-user)
2. **[P0/P1] Memories page asserts facts about the user drawn from nothing they provided** — "built from your notes and connected accounts" with no accounts and no surviving notes; novice now doubts every message (novice P0, power-user P1)
3. **[P1] Product contradicts its own pitch "remembers everything so you never start from zero"** — first screen is "Nothing here yet." with no path to fill it; Q4 = No for 2 of 2 (novice, power-user)

## Score
- **Score:** 2/10 — the product's own copy is false at the two moments that matter (save confirmation, memories), and 8 undefined terms sit between a non-technical user and the rest.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic); findings rest on personas the run invented, not researched ones
- **Not reached:** marketing page copy (promise known from pre-session line only) · Export result · toast screenshot (`04-note-saved-toast.png` shows the form, not the toast) · mobile
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect."
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | 2:41 (live preview; note then lost) | at risk | Partial | Fail |
| power-user | not reached | not reached | Partial | Fail |

- Jargon: 8 terms a non-technical reader could not explain, across signup, nav and Settings.
- Reading level of sentences: ≈ grade 5–6; the barrier is vocabulary, not syntax.
- Error copy observed: 0 (the only failure rendered as success).

## Severity flips
- Memories page (b5fd33310c0b): P0 novice — "is it making up the 'Saved' too?" · P1 power-user — "a demo panel, I assume. Not going to trust it."
- Workspace type screen (a0a9df6b0d8e): P1 novice — guessed after 43 s · P3 power-user — "Fine — I've seen worse."
- Empty state "Nothing here yet." (3853568a9ff0): P2 novice · non-issue power-user.
- Read: the copy assumes a technical reader; the pitch invites a non-technical one.

## Next action
Make "Saved ✓" wait for a 2xx and add an error message on failure, then either label the Memories content as sample or show nothing until real memories exist.
