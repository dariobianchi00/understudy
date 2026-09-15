# Nimbus Notes — onboarding — Run 2026-09-08 (fixture02)

Nobody activates: both personas reached the Save button inside 3 minutes, saw "Saved ✓" over a failed request, found an empty list, and quit — 0 of 2 reached durable value, both by abandonment before the 7-minute mark.

## Top 3
1. **[P0] "Saved ✓" toast fires while POST /api/notes returns 500, so every note is lost** — the single drop-off point for 2 of 2 personas; the run objective fails here (novice, power-user)
2. **[P0] Memories page asserts three facts about a brand-new user that are not theirs** — the novice read invented facts about herself and stopped believing anything the product said (novice; P2 for power-user)
3. **[P1] Irreversible "workspace type" choice between three unexplained terms precedes any sight of the product** — 43 s stall and a guess before the novice had seen a single screen (novice; P3 for power-user)

## Score
- **Score:** 1/10 — no persona kept a single note; the product declares success over a failed save and both users quit within 7 minutes

## Funnel

| Stage | novice | power-user |
|---|---|---|
| Reached entry point | ✓ 00:00 | ✓ 00:00 |
| Workspace created | ✓ 00:48 | ✓ ~00:25 |
| Dashboard reached | ✓ 00:55 | ✓ 00:30 |
| Note composed | ✓ 02:41 | ✓ 01:00 |
| Note persisted / findable | ✗ 03:12 | ✗ 01:00 |
| **First value reached** | ⚠ nominal 02:41 (live preview) · durable ✗ | ✗ |
| Returned to a second task | ✗ | ✗ |
| Outcome | **abandoned 06:30** | **abandoned 03:00** |

- **Steps to value (product path):** 5 · **Time to value:** not reached (novice nominal 02:41, retracted in debrief) · **Drop-off:** Save → empty dashboard
- The gap between "product said saved" and "persona got value" is the whole report: `timeline.json` logs first value at 161 s for a word counter; the persona's own Q1 answer is "right now: nothing."
- Both are abandonments, not time-outs — 06:30 and 03:00 against a 90-minute cap.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic); findings rest on personas the capture invented, not researched users
- **Not reached:** "Cards" page as a destination; "Export"; any second session; mobile
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect."
- **Models:** traversal `fixture-hand-authored` · scoring `opus`
- **Price:** none in target — TTFV judged against the consumer self-serve benchmark (<5 min healthy)

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | 02:41 nominal / durable not reached | not reached | Fail — Q1 "nothing", Q2 reaches 2, Q3 "No. Nothing" | Fail — "it lost what I gave it, and the 'memories' it does have aren't mine" |
| power-user | not reached | not reached | Fail — Q1 "Nothing yet", Q2 reaches 2 ("one of them doesn't work") | Fail — "It remembers nothing I gave it and claims things I didn't" |

## Severity flips
- Workspace-type gate: P1 for novice (43 s stall, guessed) vs P3 for power-user ("Fine — I've seen worse") — `3970a4ef2a0b-a/-b`.
- Fabricated Memories: P0 for novice (doubted "Saved" because of it) vs P2 for power-user ("a demo panel, I assume") — `77c5cc3d8f49-a/-b`.
- Empty dashboard and "Cards/block/notes" vocabulary: P2 for novice, no reaction from power-user — reported for novice only.

## Next action
- Gate the "Saved ✓" toast on a 2xx from `/api/notes` and fix the 500 — nothing else in onboarding can be measured until a note survives a save.
