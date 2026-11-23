# Nimbus Notes — ux — Run 2026-09-08 (fixture02)

Nimbus Notes fails its core job: both personas were told "Saved ✓", never found their note again, and quit.

## Top 3
1. **[P0] Save confirms success but the note never appears in list or search** — every note written was lost; both personas gave up and would pay nothing (novice, power-user)
2. **[P0] Memories page presents invented facts about the user as remembered** — novice concluded the product lies, including about "Saved"; power-user distrusted it (novice P0, power-user P1)
3. **[P2] Irreversible workspace-type choice uses undefined jargon before the user sees the product** — novice spent 43 s guessing a permanent choice (novice)

## Score
- **Score:** 1/10 — neither persona could save and find a single note, and both said they would not return

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic); findings rest on personas the agent invented
- **Not reached:** note edit/delete, Export, mobile viewport, connected accounts
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect." (auth wall always excluded)
- **Models:** traversal `fixture-hand-authored` · scoring `opus`
- **Layer B:** applies — Memories is an inferred-profile surface

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | not reached (02:41 to live preview only) | not reached | Fail | Fail |
| power-user | not reached | not reached | Fail | Fail |

- Objective "A new user can write a note and find it again": failed 2/2, `gave_up: true` both
- C-SOWHAT: Fail 2/2 — novice: "right now: nothing"; power-user: "Nothing yet — it accepts a note and then loses it."
- Findings: 2 P0 · 1 P1 · 5 P2 · 0 P3 (8 blocks, 7 issues)

## Severity flips
- Memories invented facts: P0 for novice (distrust spread to "Saved"), P1 for power-user (dismissed as demo, distrusted in debrief)
- Workspace-type jargon: P2 for novice (43 s stall, guessed); non-issue for power-user ("Fine — I've seen worse.")
- Empty dashboard: P2 for novice (expected "my stuff"); non-issue for power-user ("Expected, nothing's in it yet.")

## Next action
- Make Save store the note, or say it failed — nothing else is scoreable until a note survives.
