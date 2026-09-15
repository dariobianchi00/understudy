# Nimbus Notes — bugs — Run 2026-09-08 (fixture02)

Nimbus Notes cannot save a note — every save returns HTTP 500 while the UI shows a green "Saved ✓" — and the Memories panel presents fabricated personal facts as real, so nothing a user does in this build produces a trustworthy result.

## Top 3
1. **[P0] Save reports success but the note is never persisted** — every note is silently discarded; the user is told it worked (novice, power-user)
2. **[P0] Memories panel fabricates personal facts the user never entered** — the product states false things about the user with full confidence (novice, power-user)
3. **[P3] Uncaught ReferenceError fires on every dashboard load** — `renderGraphOverlay is not defined`, no observed visible consequence (novice, power-user)

## Score
- **Score:** 1/10 — the core action (write a note, find it again) fails on every attempt, and the product lies about it both times.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic)
- **Not reached:** Cards list view (never populated to open), any second-session or refresh check, mobile viewport
- **Excluded:** The login wall at /app/login.html — infrastructure, not a defect.
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | not reached | not reached | Fail | Fail |
| power-user | not reached | not reached | Fail | Fail |

## Severity flips
None — both bugs hit both personas at the same severity; only one persona (novice) narrated abandonment explicitly, but power-user's debrief shows the same stop condition ("Save doesn't save and search doesn't search. Nothing else matters until those work.").

## Next action
Fix `POST /api/notes` (500) and stop showing "Saved ✓" on a failed write before shipping anything else.
