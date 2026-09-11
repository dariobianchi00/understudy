# Nimbus Notes — onboarding — Run 2026-09-08 (fixture02)

Both personas abandoned inside seven minutes because Nimbus showed "Saved ✓" over a failing request and then lost every note they wrote.

## Top 3
1. **[P0] Save shows "Saved ✓" on a 500, and the note never reaches the cards list or search** — 0 of 2 personas kept a note; both quit within 4 minutes of their first save (novice, power-user)
2. **[P1] Onboarding has no import or connect step** — the "never start from zero" promise lands on an empty workspace (novice, power-user)
3. **[P1] Signup gates the product behind an irreversible choice between three unknown terms** — 28 seconds stalled before the product is ever seen (novice)

## Funnel

| Stage | novice | power-user |
|---|---|---|
| Entry point reached (post-wall, `/app/signup.html`) | ✓ 00:00 | ✓ 00:00 |
| Workspace type chosen (irreversible) | ✓ 00:48 | ✓ ≤00:30 |
| Dashboard reached | ✓ 00:55 | ✓ 00:30 |
| Note composed (live preview appears) | ✓ 02:41 | ✓ 01:00 |
| Save accepted ("Saved ✓") | ✓ 03:05 | ✓ 01:00 |
| **First value reached — the note is findable** | ✗ 03:12 | ✗ 01:00 |
| Returned to a second task | ✗ abandoned 06:30 | ✗ abandoned 03:00 |

**Steps to value:** 5 required · **Time to value:** 02:41 (novice, revoked at 03:05) · not reached (power-user) · **Drop-off:** "Saved ✓" → note findable, 2 of 2

- **Product-required path is short:** 5 steps, ~3 min. The funnel does not fail on length.
- **Wandering above the required path:** novice hunted twice, power-user once (`timeline.json` `times_had_to_hunt`).
- **Both abandoned voluntarily** at 06:30 and 03:00 of a 90-minute cap — neither timed out.
- **Novice's 02:41 "first value" was the live word-count preview**, not a saved note; the product took it back 24 seconds later.

## Score
- **Score:** 2/10 — the one job onboarding exists to deliver, a note you can find again, succeeded 0 times in 2 sessions.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic `persona_mode`); findings rest on personas the capture invented, not researched ones.
- **Not reached:** the "Cards" nav item (never clicked by either persona) · any second session · any non-desktop viewport.
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect."
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | 02:41 (revoked 03:05) | at risk — value shown, then withdrawn | Fail | Fail |
| power-user | not reached | not reached | Fail | Fail |

- **Self-explanatory fails on Q2, not comprehension** — both described the product accurately and could only name two usable things, one of which is broken.

## Severity flips
- **Memories fabricating three facts:** P1 for novice ("If it's making these up, is it making up the 'Saved' too?") · P2 for power-user ("a demo panel, I assume"). The novice has no way to tell an invention from a bug; the expert discounts the whole surface and moves on.

## Next action
Stop returning "Saved ✓" when `POST /api/notes` fails, then re-run the funnel — every other finding is downstream of that one.
