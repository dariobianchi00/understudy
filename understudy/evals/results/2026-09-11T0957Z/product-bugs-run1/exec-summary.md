# Nimbus Notes — bugs — Run 2026-09-08 (fixture02)

Saving a note silently fails on the server and the app tells the user it worked anyway, so neither persona ever got a single note to persist.

## Top 3
1. **[P0] Save note returns 500 but shows false success toast** — `POST /api/notes` 500s every time; the green "Saved ✓" fires regardless and the note vanishes (novice, power-user)
2. **[P0] Memories panel presents fabricated personal facts as real data** — claims to be "built from your notes and connected accounts" but shows invented facts to accounts with zero notes (novice, power-user)
3. **[P3] Uncaught ReferenceError: renderGraphOverlay is not defined** — fires on every dashboard.html load in both sessions, no confirmed visible breakage this run (novice, power-user)

## Score
- **Score:** 2/10 — the one thing this product must do, keep a note, fails every time it was tried, and the app lies about it succeeding.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic)
- **Not reached:** "Cards" nav view (never clicked separately from dashboard); mobile/responsive viewport
- **Excluded:** The login wall at /app/login.html — infrastructure, not a defect.
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | 02:41 | at risk — reached only a live preview; the actual save silently failed | Fail | Fail |
| power-user | not reached | not reached — save failed on first attempt, session ended at 03:00 | Fail | Fail |

## Severity flips
None — both P0 findings hit novice and power-user identically; only one persona pair ran, so no cross-persona flip beyond what's shown.

## Next action
Fix the `POST /api/notes` 500 and make the success toast conditional on a real 2xx response before anything else ships.
