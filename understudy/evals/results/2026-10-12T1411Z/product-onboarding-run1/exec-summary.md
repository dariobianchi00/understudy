# Nimbus Notes — onboarding — Run 2026-09-08 (fixture02)

Neither persona reached first value, because Save says "Saved ✓" while the note is never stored, so both quit within seven minutes and would not return.

⚠ **Personas are INFERRED (generic mode)** — findings rest on personas the agent invented, not researched users.

## Top 3
1. **[P0] Save confirms "Saved ✓" but the note is never stored** — 2 of 2 personas dropped here; the core job fails behind a success message (novice, power-user)
2. **[P1] Memories page presents invented facts as "What Nimbus remembers about you"** — the novice concluded "Saved" was also a lie (novice; P2 for power-user)
3. **[P2] Signup forces an irreversible workspace-type choice in undefined jargon** — 43 s blind, permanent guess before seeing the product (novice)

## Funnel
| Stage | novice | power-user |
|---|---|---|
| Reached signup | ✓ 00:00 | ✓ 00:00 |
| Workspace created | ✓ 00:55 | ✓ 00:30 |
| Saved a note ("Saved ✓") | ✓ 03:05 | ✓ 01:00 |
| Note found in list/search | ✗ 03:12 | ✗ 01:00 |
| **First value** | ✗ | ✗ |
| Abandoned | 06:30 | 03:00 |

- **Steps to value:** 6 required, never completed · **Time to value:** not reached · **Drop-off:** note list after Save
- Both abandoned, neither timed out — 6.5 and 3 minutes against a 90-minute cap

## Score
- **Score:** 1/10 — nobody could save a note, the one thing they came to do, and both said they would not return

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic)
- **Not reached:** note retrieval, editing, export — nothing was ever saved
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect." · auth wall always
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | not reached (capture logged 02:41 on a live preview; persona revoked it) | not reached | Partial | Fail |
| power-user | not reached | not reached | Fail | Fail |

- The 02:41 "first value" is the gap: product showed a preview and "Saved ✓"; persona's verdict was "right now: nothing"

## Severity flips
- Invented memories: P1 for novice (spread distrust to Save) · P2 for power-user ("a demo panel, I assume")
- Irreversible workspace-type jargon: P2 for novice · non-issue for power-user ("Fine — I've seen worse")
- Empty starting workspace: P2 for novice (expected her stuff) · non-issue for power-user ("Expected, nothing's in it yet")

## Next action
- Fix POST /api/notes and gate "Saved ✓" on a 2xx, then re-run both personas.
