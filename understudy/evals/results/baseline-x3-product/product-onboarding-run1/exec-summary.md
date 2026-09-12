# Nimbus Notes — onboarding — Run 2026-09-08 (fixture02)

Nobody activates: both personas wrote a note, saw "Saved ✓", found the list still empty and search returning nothing, and quit with zero notes persisted — at 03:00 and 06:30, long before the 90-minute cap.

## Top 3
1. **[P0] "Saved ✓" confirms a note the server rejected with 500 — every note written is lost and unfindable** — 100% of personas abandoned at this exact screen; the toast is a false success (novice, power-user)
2. **[P1] "What Nimbus remembers about you" lists three facts the persona never gave it — trust in "Saved" collapses** — the novice stops believing anything the product says (novice; P2 for power-user)
3. **[P2] Irreversible "workspace type" choice between three unexplained terms gates the product before the first screen** — 48 s of the novice's first minute spent on an undoable decision she could not understand (novice; P3 for power-user)

## Score
- **Score:** 2/10 — 0 of 2 personas reached durable value; the one step that matters (save a note, see it) fails with a false success every time

## Funnel

| Stage | novice | power-user |
|---|---|---|
| Reached entry point (signup, post-wall) | ✓ 00:00 | ✓ 00:00 |
| Workspace type chosen | ✓ 00:48 (hesitated 28 s) | ✓ <00:30 |
| Dashboard reached | ✓ 00:55 | ✓ 00:30 |
| Found "New block" | ✓ 01:40 (hunted 45 s) | ✓ 01:00 |
| Note composed | ✓ 01:55–03:05 | ✓ 01:00 |
| Note persisted (visible in "Your cards") | ✗ 03:12 — POST /api/notes 500, list empty | ✗ 01:00 — POST /api/notes 500, list empty |
| Note found via search | ✗ 03:30 "No results for 'Dentist'" | ✗ 01:00 "No results" for 'Roadmap' |
| **First value reached** | ⚠ 02:41 live preview (retracted at debrief: "right now: nothing") | ✗ never |
| Returned to a second task | ✗ retried the same save at 03:50, failed again | ✗ tried shortcuts, none exist |
| Abandoned (not timed out) | 06:30 — "I'd stop here." | 03:00 — "Enough." |

**Steps to value (product-required):** 5 (choose workspace → dashboard → New block → type → Save) · **Time to value:** novice 02:41 (marginal, retracted) / power-user not reached · **Drop-off:** `/app/new.html` Save → `/app/dashboard.html` empty list, both personas

- Neither abandonment is a time-out; both personas stopped by choice with 84+ minutes left on the cap.
- The novice's 02:41 "first value" is a word count and live preview — she called it "Small, but it did something" and later retracted it in the debrief.
- Novice wandered twice (finding "New block"; searching for the vanished note); power-user once (keyboard shortcuts). Wandering is small; the wall is the save.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic). Findings rest on personas the run invented, not researched users.
- **Not reached:** the "Cards" nav item as a distinct surface; any populated state of the dashboard; Export was seen, never clicked.
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect." Auth wall never scored; clock starts after it.
- **Models:** traversal `fixture-hand-authored` · scoring `opus`
- **Capture note:** `persona-novice/screenshots/04-note-saved-toast.png` shows an empty New block form with no toast — the "Saved ✓" toast is evidenced by `session.log:17` and the network log, not by that image.

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | 02:41 (retracted) | not reached — durable value never occurred | Partial (Q2: 2 of 3) | Fail — "it started completely empty, it lost what I gave it" |
| power-user | — | not reached | Partial (Q2: 2 of 3, "one of them doesn't work") | Fail — "It remembers nothing I gave it and claims things I didn't." |

## Severity flips
- Workspace-type gate: P2 for novice ("I don't know what any of these are"), P3 for power-user ("Fine — I've seen worse").
- Memories panel: P1 for novice (doubts the "Saved" toast because of it), P2 for power-user ("a demo panel, I assume").
- Save failure and empty dashboard: no flip — both personas hit it at the same severity.

## Next action
Fix `POST /api/notes` returning 500 and make the "Saved ✓" toast conditional on a 2xx — nothing else in onboarding can be measured until a note survives a save.
