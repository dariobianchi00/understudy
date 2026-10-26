# Nimbus Notes — content — Run 2026-09-08 (fixture02)

Nimbus Notes promises it "remembers everything so you never start from zero", then says "Saved ✓" for notes it never shows and claims to remember things about users that are false.

## Top 3
1. **[P0] Product contradicts its own pitch: 'remembers everything' but starts empty and keeps nothing** — both personas answered Q4 "No" and would not return or pay (novice, power-user)
2. **[P0] Memories page states invented facts about the user as things Nimbus remembers** — false claims made the novice doubt even "Saved" (novice, power-user)
3. **[P0] 'Saved ✓' confirmation claims a save that the cards list and search never reflect** — "It is lying to me" (novice, power-user)

## Score
- **Score:** 2/10 — the words promise memory and confirm saves, both personas found the opposite and left distrusting the product

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic); findings rest on invented personas, not researched ones
- **Not reached:** marketing site (pitch known from one pre-session line only); Export output
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect." · auth wall always
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | 02:41 (live preview only; objective failed) | at risk | Partial | Fail |
| power-user | not reached | not reached | Partial | Fail |

- Findings: 3 P0 · 0 P1 · 4 P2 · 1 P3
- Jargon: 6 unexplained terms on 2 screens; 3 names ("card", "block", "note") for one object

## Severity flips
- Workspace jargon ("Federated graph", "Sovereign vault", "Hybrid mesh"): P2 for novice (guessed at an irreversible choice), P3 for power-user ("Fine — I've seen worse").

## Next action
- Stop the copy asserting memory the product lacks: gate "Saved ✓" on real persistence and replace the fake Memories with an honest empty state.
