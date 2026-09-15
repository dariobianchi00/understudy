# Nimbus Notes — onboarding — Run 2026-09-08 (fixture02)

Nobody activates: both personas wrote a note, saw "Saved ✓", found the list empty and search blank, and quit inside 7 minutes.

## Top 3
1. **[P0] Save shows "Saved ✓" but the note is never listed or searchable; both personas abandon here** — the one thing the product exists to do fails silently; 2/2 personas leave with zero notes and zero trust (novice, power-user)
2. **[P1] Memories page asserts facts that are not the persona's, and both stop trusting "Saved"** — after the lost note, invented "memories" turn a bug into a credibility collapse; both say they will not trust it (novice, power-user)
3. **[P1] Irreversible workspace-type choice between three undefined terms stalls the novice 48s before any value** — first screen after signup demands an unexplained, permanent decision; the novice guesses (novice)

## Score
- **Score:** 2/10 — 0 of 2 personas reached durable value; the only useful moment (live preview at 02:41) was revoked 31s later when the note vanished.

## Funnel

| Stage | novice | power-user |
|---|---|---|
| Reached entry point (post-wall) | ✓ 00:00 | ✓ 00:00 |
| Workspace type chosen (irreversible) | ✓ 00:48 | ✓ 00:30 |
| Dashboard reached | ✓ 00:55 | ✓ 00:30 |
| Found "New block" | ✓ 01:40 (2 hunts) | ✓ 01:00 |
| Note composed | ✓ 02:41 | ✓ 01:00 |
| "Saved ✓" shown | ✓ 03:05 | ✓ 01:00 |
| Note listed / searchable | ✗ 03:12 · ✗ 03:30 · ✗ retry 03:50 | ✗ 01:00 |
| **First value reached** | ✓ 02:41 (live preview) — revoked 03:12 | ✗ |
| Abandoned (declared, not timed out) | 06:30 | 03:00 |
| Returned to a second task | ✗ | ✗ |

**Steps to value:** 5 required (workspace type → dashboard → New block → type → Save) · **Time to value:** 02:41 novice / not reached power-user · **Drop-off:** Save → dashboard, both personas

- Both exits are abandonment, not time-out: cap was 90 min; novice left at 06:30, power-user at 03:00.
- Novice retried the save once (03:50) before declaring "It is lying to me."
- Power-user hit the same wall at 01:00 and spent the remaining 2 min confirming nothing else mattered.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic); findings rest on personas the run invented, not researched users
- **Not reached:** any state with a persisted note; Cards list with content; search with results; Export output
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect."
- **Models:** traversal `fixture-hand-authored` · scoring `opus`
- **Evidence caveat:** `persona-novice/screenshots/04-note-saved-toast.png` shows a blank New block form, not the toast; the toast rests on `session.log:17` and the network record only

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | 02:41 (timeline: 161s, 5 steps, 2 hunts) | at risk — value revoked at 03:12, note never persisted | Partial (Q2 names 2) | Fail |
| power-user | not reached (timeline: null, 0 steps) | not reached | Partial (Q2 names 2, "one of them doesn't work") | Fail |

## Severity flips
- Workspace-type screen (`/app/signup.html`): **P1 novice** ("I don't know what any of these are") vs **P3 power-user** ("Fine — I've seen worse"). The product has picked an expert user without saying so.

## Next action
Make `POST /api/notes` persist and show the note in "Your cards" on return — nothing else in this funnel can be measured until it does.
