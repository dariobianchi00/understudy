# Nimbus Notes — onboarding — Run 2026-09-08 (fixture02)

Neither persona reached first value: both wrote a note, were told "Saved ✓" while the server returned 500, found nothing, and quit within seven minutes.

## Top 3
1. **[P0] Save confirms success while the server rejects the note, so no persona ever kept a note** — 2 of 2 personas abandoned at this step; funnel ends here (novice, power-user)
2. **[P1] Memories page asserts invented facts about a brand-new user, collapsing trust in every other confirmation** — turned a bug into "it is lying to me" (novice, power-user)
3. **[P2] Empty dashboard offers no next step, contradicting the never-start-from-zero promise** — novice spent 45 s searching an empty workspace (novice)

## Score
- **Score:** 1/10 — nobody could keep a single note; both personas quit and said they would pay nothing

## Funnel
| Stage | novice | power-user |
|---|---|---|
| Dashboard reached | ✓ 00:55 | ✓ 00:30 |
| Save clicked | ✓ 03:05 | ✓ 01:00 |
| Note persisted | ✗ 500 | ✗ 500 |
| **First value** | ✗ abandoned 06:30 | ✗ abandoned 03:00 |

- **Steps to value:** 5 required · **Time to value:** not reached · **Drop-off:** Save on `/app/new.html`

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic); findings rest on invented personas
- **Not reached:** saved-note search, Export, second task
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect."
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | not reached (capture logged 02:41 for a live preview — not value) | not reached | Fail | Fail |
| power-user | not reached | not reached | Fail | Fail |

## Severity flips
- Irreversible workspace-type choice: P2 for novice (43 s, guessed) · P3 for power-user ("Fine — I've seen worse").

## Next action
Fix `POST /api/notes` and gate "Saved ✓" on a 2xx, then re-run both personas.
