# Nimbus Notes — bugs — Run 2026-09-08 (fixture02)

Saving a note returns a 500, the UI shows a success toast anyway, and the note is never stored or searchable — both personas hit this on their first save and neither would pay for the product afterward.

## Top 3
1. **[P0] Save reports success while POST /api/notes fails with 500 and the note is never stored** — core objective fails for 100% of personas; both said they would not return (novice, power-user)
2. **[P1] Memories panel fabricates personal facts and deepens the novice's distrust of the save toast** — novice explicitly doubts "Saved" is also a lie because of it (novice)
3. **[P2] Memories panel fabricates personal facts the power-user writes off as a demo panel** — dismissed without abandonment, but named as a trust hit in debrief (power-user)

## Score
- **Score:** 2/10 — the one flow both personas were sent to complete (write a note, find it again) fails outright, and the "Saved ✓" toast actively lies about it.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic persona_mode; findings rest on personas the run invented, not researched ones)
- **Not reached:** Cards/list view with any real content, note editing, note deletion, mobile viewport
- **Excluded:** The login wall at /app/login.html — infrastructure, not a defect.
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | 2:41 (nominal — note later found unsaved) | at risk | Fail | Fail |
| power-user | not reached | at risk | Fail | Fail |

## Severity flips
- Memories panel fabricating personal facts: **P1** for novice (explicitly linked to doubting the save toast, cited in debrief as part of why the product doesn't match its promise) vs **P2** for power-user (dismissed as "a demo panel," noted in debrief but did not change behavior in-session). Same defect, different observed impact — see findings `151eda485577` / `f1d1125965d9`.

## Next action
Fix the /api/notes 500 and make the save UI reflect the real request outcome before touching anything else — nothing downstream (search, Cards list, trust in Memories) can be evaluated until notes actually persist.
