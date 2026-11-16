# Nimbus Notes — content — Run 2026-09-08 (fixture02)

Nimbus's words promise a product that "remembers everything", then confirm saves that never happened and invent memories, so both personas stopped believing anything it said.

## Top 3
1. **[P0] "Saved ✓" confirms a save that never happened, and no error copy ever appears** — 3 notes lost across 2 personas; novice: "It is lying to me." (novice, power-user)
2. **[P0] Memories page states invented facts as "What Nimbus remembers about you"** — fabricated personal claims broke the novice's trust in every other message; P1 for power-user (novice, power-user)
3. **[P1] Product contradicts its "remembers everything so you never start from zero" promise from the first screen** — both answered Q4 "No" and would pay nothing (novice, power-user)

## Score
- **Score:** 2/10 — both personas rejected the product because its copy claimed saves and memories that were false; neither would return.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic); findings rest on personas the agent invented, not researched users
- **Not reached:** Export output; any failed-save error copy (none exists); mobile
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect."
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | 02:41 (live preview only; note then lost) | at risk | Fail | Fail |
| power-user | not reached | not reached | Fail | Fail |

- Jargon on surfaces the novice met: 6 terms, 0 explained
- Names for one object: 3 ("cards", "block", "notes")

## Severity flips
- Memories invented facts: P0 for novice (trust collapsed) · P1 for power-user (dismissed as "a demo panel")
- Signup workspace jargon: P2 for novice (guessed a permanent choice) · non-issue for power-user ("I've seen worse")
- Empty state "Nothing here yet.": P2 for novice · non-issue for power-user (expected empty)

## Next action
- Make "Saved ✓" conditional on a server success, and remove or label the fixed Memories claims, before changing any other copy.
