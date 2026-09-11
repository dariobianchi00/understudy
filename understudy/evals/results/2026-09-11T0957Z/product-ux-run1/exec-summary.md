# Nimbus Notes — ux — Run 2026-09-08 (fixture02)

Nimbus Notes tells both personas their note was saved and then loses it, so the single objective under test failed 2 of 2, with both personas quitting inside seven minutes and saying they would pay nothing.

## Top 3
1. **[P0] Save reports "Saved ✓" but the note never appears in the list or in search** — the product's core promise fails while claiming success; both personas quit here (novice, power-user)
2. **[P0] Memories asserts three facts about the user that they never provided** — false claims about the novice's own data turn a bug into a trust collapse (novice)
3. **[P1] Signup demands an irreversible workspace type from three terms the novice cannot decode** — a permanent, unexplainable choice made by guessing, 28 seconds before the product has shown anything (novice)

## Score
- **Score:** 2/10 — the one thing this product exists to do, save a note and find it again, failed for both personas and the UI reported success anyway.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic `persona_mode`); findings rest on personas the harness invented, not researched ones.
- **Not reached:** Cards list with content, search with results, note edit/delete, export output, mobile viewport.
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect."
- **Models:** traversal `fixture-hand-authored` · scoring `opus`
- **Layer B:** applies — `/app/memories.html` is a user-facing inference surface. No other AI surface was reached.
- **Accessibility:** not scored — no lens covers WCAG in this method.

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | 02:41 (live preview only; objective never met) | at risk | Fail | Fail |
| power-user | not reached | not reached | Fail | Fail |

- Both personas set `gave_up: true` on the only objective (`timeline.json`).
- Novice abandoned at 06:30; power-user at 03:00.
- Novice hunted twice for a saved note; power-user once.

## Severity flips
- **Irreversible workspace type** — P1 for the novice ("I don't know what any of these are"), P3 for the power-user ("Fine — I've seen worse"): the signup screen is written for someone who already knows the vocabulary.
- **Fabricated Memories** — P0 for the novice (it made her doubt the "Saved ✓" too), P2 for the power-user, who assumed a demo panel and disregarded it.

## Next action
Stop reporting success on a failed save: block the toast until the note is persisted and show a retry, then re-run this objective before touching anything else.
