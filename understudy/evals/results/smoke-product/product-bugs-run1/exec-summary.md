# Nimbus Notes — bugs — Run 2026-09-08 (fixture02)

Nimbus Notes cannot save a note and tells the user it did, while its "Memories" feature fabricates facts about a user who has entered nothing — both personas hit the data-loss bug and gave up within four minutes.

## Top 3
1. **[P0] Save reports success while the note is silently discarded** — every note ever written in this run vanished after a green "Saved ✓" toast (novice, power-user)
2. **[P0] Memories panel invents personal facts the user never entered** — "Your team uses Jira and Slack" shown to a workspace with zero notes and zero connected accounts (novice, power-user)
3. **[P3] Uncaught ReferenceError on every dashboard load: `renderGraphOverlay is not defined`** — repeats on every dashboard visit, no observed effect on rendering (novice, power-user)

## Score
- **Score:** 1/10 — the one thing the product promises (remember your notes) fails outright, with a fabricated-memory panel making it worse, not better

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic, per manifest `persona_mode`)
- **Not reached:** nothing beyond the two personas' explored surfaces; both stopped within 7 minutes after the save/search failure
- **Excluded:** The login wall at /app/login.html — infrastructure, not a defect (per manifest scope exclusions)
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | not reached (161s spent, save never persisted) | at risk | Fail | Fail |
| power-user | not reached | at risk | Fail | Fail |

## Severity flips
- None observed — the save failure and the fabricated-memories bug hit both personas identically and at the same severity.

## Next action
Fix `POST /api/notes` (returns 500) and stop showing "Saved ✓" until the server confirms persistence; that single fix unblocks the objective for both personas.
