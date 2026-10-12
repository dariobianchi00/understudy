# Nimbus Notes — ux — Run 2026-09-08 (fixture02)

Neither persona could keep a single note, because Save reports success while nothing appears, and a Memories page full of invented facts made both stop trusting it.

## Top 3
1. **[P0] Save confirms with a success toast but the note never appears in the cards list or search** — every note written was lost; both personas gave up on the core objective (novice, power-user)
2. **[P0] Memories page asserts invented facts about the user, and the novice extends that distrust to Save** — false claims made her doubt every message the product shows (novice)
3. **[P1] Memories page asserts invented facts that the power user writes off as a demo and will not trust** — the headline "remembers everything" feature reads as fake (power-user)

## Score
- **Score:** 2/10 — neither persona could save and find a note; both said they would not use or pay for it.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic); findings rest on personas the agent invented
- **Not reached:** saved-note retrieval, note edit/delete, Export output, mobile
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect." Auth wall always excluded.
- **Models:** traversal `fixture-hand-authored` · scoring `opus`
- **Evidence caveat:** 3 screenshots do not show what their filenames claim; those claims rest on session logs (see Dropped list)

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | not reached (preview at 02:41; save failed) | not reached | Fail | Fail |
| power-user | not reached | not reached | Fail | Fail |

## Severity flips
- Memories page with invented facts: P0 for novice (distrust spread to Save) · P1 for power-user (dismissed as demo, would not trust).
- Irreversible workspace-type choice: P2 for novice (28 s blind guess) · non-issue for power-user ("I've seen worse").

## Next action
- Make Save persist and show the note on the dashboard before touching anything else.
