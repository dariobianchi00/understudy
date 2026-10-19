# Nimbus Notes — ux — Run 2026-09-08 (fixture02)

Nimbus Notes fails its one job: both personas saved a note, were told "Saved ✓", never found it again, and quit.

## Top 3
1. **[P0] Save shows "Saved ✓" but the note never appears in cards or search** — both personas gave up on the objective within 4 minutes (novice, power-user)
2. **[P0] Memories page asserts invented facts about the novice, and she stops trusting "Saved"** — invented claims turned a bug into total distrust (novice)
3. **[P1] Memories page asserts facts the power user never gave, and he writes the panel off** — the headline "remembers everything" feature reads as fake (power-user)

## Score
- **Score:** 2/10 — neither persona could keep a note, and both said they would not return or pay

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic); findings rest on personas the agent invented
- **Not reached:** Export (never clicked), note edit/delete, "Cards" nav item, mobile
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect." Auth wall always.
- **Models:** traversal `fixture-hand-authored` · scoring `opus`
- **Layer B:** applied only to the "Memories" surface; no other AI surface observed

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | 02:41 (live preview only; saved note never reached) | not reached | Fail | Fail |
| power-user | — | not reached | Fail | Fail |

- Objective "A new user can write a note and find it again": failed, `gave_up: true` for 2 of 2 personas
- Severity count: P0 2 · P1 1 · P2 5 · P3 0

## Severity flips
- Memories invented facts: P0 for novice (spread distrust to "Saved") · P1 for power-user (dismissed as "a demo panel").
- Irreversible workspace-type choice: P2 for novice (43 s guessing) · non-issue for power-user ("I've seen worse").

## Next action
- Make "Saved ✓" conditional on a confirmed save, and blank the Memories page until real notes exist.
