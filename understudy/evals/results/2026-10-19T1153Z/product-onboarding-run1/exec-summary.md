# Nimbus Notes — onboarding — Run 2026-09-08 (fixture02)

Neither persona reached first value: both wrote a note, saw "Saved ✓", found an empty list, and quit within 7 minutes.

> ⚠ **Generic personas.** Findings rest on INFERRED personas (novice, power-user), not researched ones.

## Top 3
1. **[P0] Save reports "Saved ✓" while POST /api/notes fails with 500, so no note survives** — 3 of 3 saves lost, 0 of 2 activated, both quit here (novice, power-user)
2. **[P1] Memories page presents invented facts as "What Nimbus remembers about you"** — it turned the lost note into "it is lying to me", and the novice stopped (novice, power-user)
3. **[P2] Signup forces an irreversible workspace-type choice in unexplained jargon before the product is seen** — the novice guessed after 43 s on screen one (novice)

## Score
- **Score:** 1/10 — neither persona could keep a single note, and both left saying they would pay nothing

## Funnel
| Stage | novice | power-user |
|---|---|---|
| Workspace created | ✓ 00:55 | ✓ 00:30 |
| Note written | ✓ 01:55 | ✓ 01:00 |
| Note persisted | ✗ (POST 500 ×2) | ✗ (POST 500) |
| **First value: note found again** | ✗ | ✗ |
| Outcome | Abandoned 06:30 | Abandoned 03:00 |

- **Steps to value:** 5 required, then the path is broken · **Time to value:** not reached · **Drop-off:** the empty "Your cards" list right after "Saved ✓"
- Both personas abandoned; neither timed out. Each had more than 84 minutes left of the 90-minute cap.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic)
- **Not reached:** a stored note, search on real content, Export, a second session
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect."
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | 02:41 preview moment, retracted | not reached | Partial | Fail |
| power-user | — | not reached | Fail | Fail |

## Severity flips
- Workspace-type choice at signup: P2 for the novice (43 s, a guess), a non-issue for the power-user ("Fine — I've seen worse").
- Empty dashboard with no next step: P2 for the novice (searched an empty product first), a non-issue for the power-user.

## Next action
Fix `POST /api/notes`, and gate "Saved ✓" on a 2xx response. Nothing else in onboarding matters until a note survives.
