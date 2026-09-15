# Nimbus Notes — content — Run 2026-09-08 (fixture02)

Nimbus promises to "remember everything" and then tells both personas two things that are not true — "Saved ✓" on a note it lost, and "What Nimbus remembers about you" on a workspace it knows nothing about — so the copy is not merely unclear, it is untrusted.

## Top 3
1. **[P0] "Saved ✓" confirms a save the server rejected, and no error copy ever appears** — both personas lost their first note behind a success message; "It is lying to me." (novice, power-user)
2. **[P0] "What Nimbus remembers about you" lists three facts about the user that are invented** — false statements about the persona's own life, captioned as built "from your notes"; P1 for the power-user who assumed demo content (novice, power-user)
3. **[P1] The product contradicts its pitch: "remembers everything" opens on "Nothing here yet." and forgets the first note** — Q4 "No" from both personas; Q3 "Nothing" from both (novice, power-user)

## Score
- **Score:** 2/10 — the product's two most important messages are false, and every other content defect (jargon signup, three names for one object, opaque settings) is downstream of a pitch the product cannot back.

## Also worth knowing
- Sentence-level reading difficulty is low; the problem is vocabulary: 5 undefined terms before first value, 3 of 4 Settings controls.
- Copy that worked: "0 words" / "Preview below" gave the novice her only moment of value; "Export — Markdown, all cards" was the one Settings line both understood.
- 9 finding blocks (7 issues, 2 split by persona): 2 P0, 3 P1, 3 P2, 1 P3.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic)
- **Not reached:** marketing site, "Cards" nav item, Export result, any screen past 07:00
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect."
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | 02:41 (live preview only; no note ever saved) | healthy on the clock, not on substance | Fail — Q2 reached 2 of 3, Q1 "right now: nothing" | Fail |
| power-user | not reached | not reached | Fail — Q2 "That's two, and one of them doesn't work" | Fail |

## Severity flips
- Invented memories: P0 novice (doubted every other message) → P1 power-user (dismissed as demo, still refused to trust).
- Undefined workspace-type choice: P1 novice (48 s guessing an irreversible decision) → P3 power-user ("I've seen worse").
- Empty state with no next step: P2 novice → non-issue power-user, who went straight to search.

## Next action
Make "Saved ✓" and the Memories page true before touching any other copy — every other content fix is polish on a product that currently lies.
