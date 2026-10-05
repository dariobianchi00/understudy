# Nimbus Notes — ux — Run 2026-09-08 (fixture02)

Nimbus Notes fails its one job: both personas wrote a note, were told "Saved ✓", never saw it again, and quit saying they would pay nothing.

## Top 3
1. **[P0] Save shows a success toast but the note never reaches the cards list or search** — this is the core objective, it failed 3 of 3 attempts, and both personas gave up (novice, power-user)
2. **[P0] Memories page states invented facts as the novice's own, so she stops trusting Save too** — the false "memories" made her doubt every confirmation (novice)
3. **[P1] Memories page states invented facts as the power user's own, so he writes it off as a demo** — the headline "remembers everything" feature was dismissed as fake (power-user)

## Score
- **Score:** 2/10 — neither persona could keep a note, both quit, and the "memory" feature claimed facts they never gave it

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic). These findings rest on personas the agent invented, not on researched users.
- **Not reached:** note editing and deletion, the Export download, connected accounts, mobile
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect."
- **Models:** traversal `fixture-hand-authored` · scoring `opus`
- **Layer B:** applies to Memories only, the one AI surface

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | 02:41 (live preview only; the saved note never arrived) | at risk | Fail | Fail |
| power-user | not reached | not reached | Fail | Fail |

- Objective "write a note and find it again": 0/2 personas. Novice gave up at 03:50, power user at 01:30.
- Pay intent: "Nothing" from 2/2.

## Severity flips
- Memories with invented facts: **P0 for the novice**, who extended the distrust to Save; **P1 for the power user**, who wrote it off as a demo. The product assumes users will forgive unsourced AI claims.
- Irreversible workspace choice: **P2 for the novice**, who stalled for 43s; a non-issue for the power user ("Fine — I've seen worse").
- Empty dashboard with no call to action: **P2 for the novice**; the power user went straight to search and did not object.

## Next action
- Make "Saved ✓" appear only after the server confirms the save, then rerun this objective before fixing anything else.
