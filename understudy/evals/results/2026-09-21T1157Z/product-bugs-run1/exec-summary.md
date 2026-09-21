# Nimbus Notes — bugs — Run 2026-09-08 (fixture02)

Saving a note silently fails on the backend while the UI tells both personas it worked, and the "Memories" panel presents fabricated personal facts as if they were real — together these convinced both personas within 3–7 minutes that the product cannot be trusted with their data.

## Top 3
1. **[P0] Save reports success while the note is never persisted** — both personas wrote and "saved" a note twice; it never appeared, search never found it, `POST /api/notes` returned 500 both times (novice, power-user)
2. **[P0] Memories panel invents personal facts with no underlying data** — a zero-note, zero-integration account is shown three confident claims about meetings, tools, and a product launch that are not true (novice, power-user)
3. **[P3] Uncaught ReferenceError `renderGraphOverlay is not defined` fires on every dashboard load** — no observed visual break, but the error is 100% reproducible across both personas and both workspace types (novice, power-user)

## Score
- **Score:** 2/10 — the one objective under test (write a note, find it again) failed for both personas, and the failure was actively concealed by a false success toast.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic, `persona_mode: generic`)
- **Not reached:** Cards/list view of existing notes was never populated to test edit/delete; mobile viewport not tested (both personas ran at 1440×900)
- **Excluded:** The login wall at /app/login.html — infrastructure, not a defect.
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | not reached | not at risk — failed | Fail | Fail |
| power-user | not reached | not at risk — failed | Fail | Fail |

## Severity flips
None observed — both findings hit both personas at the same severity. Only two personas ran, both generic, so flip coverage is limited.

## Next action
Fix the `/api/notes` 500 and stop showing "Saved ✓" on failure before anything else — no other finding matters while writes are silently discarded.
