# Nimbus Notes — bugs — Run 2026-09-08 (fixture02)

Saving a note fails on the server every time, the UI reports success anyway, and the app then shows the user fabricated personal facts it never collected — both personas gave up within four minutes having saved nothing.

## Top 3
1. **[P0] Save reports success while POST /api/notes returns 500 and the note is never persisted** — every save is silently discarded; the core objective (write a note, find it again) fails 100% of attempts (novice, power-user)
2. **[P0] Memories panel presents fabricated personal claims as fact with zero real notes saved** — invents a Tuesday-meeting habit, a Jira/Slack stack and a Q4 launch for users who saved nothing, breaking trust irreparably (novice, power-user)
3. **[P3] Uncaught ReferenceError: renderGraphOverlay is not defined fires on every dashboard load** — recurring JS exception on the app's main screen, no confirmed visible symptom this run (novice, power-user)

## Score
- **Score:** 1/10 — the one objective under test (write a note, find it again) fails for both personas, and the failure is actively hidden behind a false success toast.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic, `persona_mode: generic`)
- **Not reached:** Cards list view was never populated because no save ever persisted; no data existed to test whether search or the cards list work when notes are actually present.
- **Excluded:** The login wall at /app/login.html — infrastructure, not a defect.
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | not reached (161s to a save that didn't persist) | not reached | Fail | Fail |
| power-user | not reached | not reached | Fail | Fail |

## Severity flips
None — both P0s hit both personas at the same severity; both gave up for the same reason (`session.log` novice 06:30 "I'd stop here", power-user 03:00 "Nothing else matters until those work.").

## Next action
Fix the POST /api/notes 500 and stop showing "Saved ✓" until the server confirms persistence — everything else in this report is unreachable until that works.
