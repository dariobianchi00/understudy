# Nimbus Notes — onboarding — Run 2026-09-08 (fixture02)

Neither persona activated, because Save shows "Saved ✓" while the server returns 500, so both abandoned within seven minutes with no note kept.

## Top 3
1. **[P0] Note save shows "Saved ✓" but the server rejects it, so every first note is lost** — 2/2 personas abandoned at this step; objective failed for both (novice, power-user)
2. **[P1] Memories page asserts facts about the user that they never gave it** — novice: "is it making up the "Saved" too?" — and she stopped two minutes later (novice; P2 for power-user)
3. **[P2] Irreversible workspace-type choice is demanded before the user has seen the product** — 43 s of guessing between three undefined options on screen one (novice)

## Score
- **Score:** 1/10 — no persona kept a single note; both quit at Save, and the core write-then-find job fails every time

## Funnel
| Stage | novice | power-user |
|---|---|---|
| Reached entry point (after wall) | ✓ 00:00 | ✓ 00:00 |
| Workspace type chosen | ✓ 00:48 | ✓ by 00:30 |
| Dashboard reached | ✓ 00:55 | ✓ 00:30 |
| Note typed in New block | ✓ 01:55 | ✓ 01:00 |
| Capture-recorded first value (live preview) | ✓ 02:41 | ✗ |
| **Note saved and visible** | ✗ 03:12 | ✗ 01:00 |
| Note found by search | ✗ 03:30 | ✗ 01:00 |
| Returned to a second task | ✗ abandoned 06:30 | ✗ abandoned 03:00 |

- **Steps to value (required):** 5 · **Time to value:** not reached durably · **Drop-off:** Save, `/app/new.html`
- Both were **abandonments**, not time-outs — 06:30 and 03:00 of a 90-minute cap
- **"Saved ✓" ≠ value:** the product declared success twice to the novice; her debrief Q1: "right now: nothing"

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic); findings rest on invented personas, not researched ones
- **Not reached:** any second task; Export never clicked; mobile
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect."
- **Models:** traversal `fixture-hand-authored` · scoring `opus`
- Two screenshots do not show what their names claim (novice `04-note-saved-toast.png`, power-user `03-search-empty.png`); those moments rest on session.log

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | 02:41 recorded (preview); revoked in debrief | not reached | Partial | Fail |
| power-user | — | not reached | Fail | Fail |

## Severity flips
- Memories fabricated facts: **P1 novice** (fed her distrust, then she quit) vs **P2 power-user** (dismissed as "a demo panel")
- Irreversible workspace choice: **P2 novice** (43 s guessing) vs non-issue power-user ("Fine — I've seen worse")

## Next action
- Fix POST /api/notes and gate "Saved ✓" on a 2xx response — nothing else in onboarding matters until a note survives Save.
