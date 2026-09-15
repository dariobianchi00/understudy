# Nimbus Notes — onboarding — Run 2026-09-08 (fixture02)

Both personas completed signup in under a minute, wrote a note, were told "Saved ✓", and then watched it vanish — activation is 0 of 2, and both quit voluntarily inside seven minutes.

## Funnel

| Stage | novice | power-user |
|---|---|---|
| Reached entry point (post-wall) | ✓ 00:00 | ✓ 00:00 |
| Workspace type chosen (irreversible) | ✓ 00:48 | ✓ ~00:20 |
| Workspace created → dashboard | ✓ 00:55 | ✓ 00:30 |
| Found the compose surface ("New block") | ✓ 01:55 | ✓ 01:00 |
| Product confirmed "Saved ✓" | ✓ 03:05 | ✓ 01:00 |
| Note visible in list or search | ✗ 03:12 | ✗ 01:30 |
| **First value reached (retained)** | ✗ | ✗ |
| Returned to a second task | ✗ abandoned 06:30 | ✗ abandoned 03:00 |

**Steps to value (required):** 5 · **Time to value:** not reached (novice measured 02:41 on an in-editor preview that did not survive Save) · **Drop-off:** the Save → list/search step, `/app/new.html` → `/app/dashboard.html`

- Both personas **abandoned**; neither timed out. They stopped at 7% and 3% of the 90-minute cap.
- Novice took 8 further actions after the first failed save; the product required none of them.

## Top 3
1. **[P0] Save confirms success and the note never appears** — the run's single objective fails for both personas; the product is not a notes app for anyone this session (novice, power-user)
2. **[P1] Memories asserts three facts about a user who has written nothing** — turns a bug into a trust collapse; the novice then doubted the "Saved" message too (novice, power-user)
3. **[P1] Signup demands an irreversible workspace-type choice before the product is seen** — 28 seconds of stalled anxiety and a guessed answer, at step one (novice)

## Score
- **Score:** 2/10 — zero of two personas retained a single note; the product reports success it did not deliver, and both users left in under seven minutes.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic `persona_mode`); findings rest on personas the capture invented, not researched users.
- **Not reached:** any second session · any surface past Settings/Memories · mobile or tablet viewports · the Export flow (seen, never clicked)
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect."
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | 02:41 (preview only; not retained) | not reached | Fail | Fail |
| power-user | not reached | not reached | Fail | Fail |

- Permission prompts: 0 for both — nothing here is a consent problem.
- Hunt events: novice 2, power-user 1.

## Severity flips
- **Irreversible workspace-type gate:** P1 for novice ("I don't know what any of these are… it wants a decision I can't undo"), non-issue for power-user ("Fine — I've seen worse"). The product has quietly picked the technical user without saying so; it is reported scoped to novice, not averaged.
- **The save failure does not flip:** P0 for both, and it ends both sessions.

## Next action
Fix `POST /api/notes` (500 on every attempt) and never render "Saved ✓" on a non-2xx response — nothing else in this funnel matters until a note survives.
