# Nimbus Notes — onboarding — Run 2026-09-08 (fixture02)

Both personas abandoned inside seven minutes with zero notes saved, because Nimbus shows a green "Saved ✓" for a save that never happened — the funnel ends at the one step the product exists to perform.

## Top 3
1. **[P0] "Saved ✓" confirms a save that never happens** — 100% drop-off at the objective step; both personas quit within 3 minutes of hitting it (novice, power-user)
2. **[P1] Fabricated "memories" turned a save bug into a trust collapse** — the novice stopped believing any product statement, including "Saved" (novice)
3. **[P2] Empty dashboard names no next step** — 60 seconds of hunting between account creation and finding the editor (novice)

## Score
- **Score:** 2/10 — neither persona completed the run's single objective, both said they would not pay, and the product confirmed a save it never performed.

## Funnel

| Stage | novice | power-user |
|---|---|---|
| Reached entry point (post-wall signup) | ✓ 00:00 | ✓ 00:00 |
| Workspace type chosen (irreversible) | ✓ 00:48 | ✓ ≤00:30 |
| Dashboard reached | ✓ 00:55 | ✓ 00:30 |
| Editor found | ✓ 01:55 | ✓ 01:00 |
| Note composed | ✓ 02:41 | ✓ 01:00 |
| **First value reached** | ✓ 02:41 (live preview only) | ✗ never |
| Note saved and retrievable (the objective) | ✗ abandoned 03:50 | ✗ abandoned 01:30 |
| Returned to a second task | ✗ quit 06:30 | ✗ quit 03:00 |

**Steps to value:** 5 required · **Time to value:** 02:41 (novice), not reached (power-user) · **Drop-off:** Save → "Your cards"

- **Both are abandonments, not time-outs** — 06:30 and 03:00 against a 90-minute cap.
- **The only value moment was a word-count preview** (`session.log:16`), not the objective.
- **Wandering on top of the required path:** novice hunted twice, power-user once (`timeline.json` `times_had_to_hunt`).

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (`persona_mode: generic`); findings rest on personas the capture invented, not researched users.
- **Not reached:** anything past the first save — no second session, no mobile, no editing or deleting an existing card.
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect."
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | 02:41 | healthy clock, objective failed | Partial | Fail |
| power-user | not reached | not reached | Fail | Fail |

## Severity flips
- **"Memories" shows facts about a user it has never met** — P1 for the novice (trust collapsed, generalised to "Saved"), P2 for the power-user (dismissed it as "a demo panel, I assume").
- **Irreversible workspace type** — 28 seconds of visible hesitation for the novice, "Fine — I've seen worse" for the power-user; the product has picked the technical user without saying so.

## Next action
Fix the 500 on `POST /api/notes` and stop the client showing "Saved ✓" on a non-2xx response — nothing else in this funnel matters until a note survives.
