# Nimbus Notes — content — Run 2026-09-08 (fixture02)

Nimbus Notes tells one story on the way in and the opposite on the way through: it promises to remember everything, then opens on a blank screen, confirms a save that did not happen, and presents three invented facts as the user's own memories.

## Top 3
1. **[P0] "Memories" asserts three facts about the user that are not theirs** — both personas stopped believing anything the product said about their data (novice, power-user)
2. **[P0] "Saved ✓" is the only copy about persistence and it is false** — novice read it twice, then quit calling the product a liar (novice, power-user)
3. **[P1] No copy reconciles "never start from zero" with an empty, hand-filled notes app** — both personas answered Q4 "no" (novice, power-user)

## Score
- **Score:** 3/10 — the product's words contradict its pitch and its own behaviour; two of nine findings are trust-breaking falsehoods in copy, and both personas quit inside seven minutes.

## Promise vs delivery
| Persona | Arrived expecting | Product delivered | Match | Cost |
|---|---|---|---|---|
| novice | "remembers everything so you never start from zero" | Empty dashboard, manual form, two lost notes, three memories that are not hers | Fail | Quit at 06:30 with zero notes saved |
| power-user | "remembers everything so you never start from zero" | Empty dashboard, manual form, one lost note, no keyboard entry | Fail | Quit at 03:00, will not trust the product |

- Both personas' own Q4 answers say "No" — my reading and theirs agree.
- The mismatch is the root cause: the one surface that echoes the pitch ("Memories") is populated with content the personas never supplied.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic persona_mode); findings rest on personas the harness invented, not researched ones
- **Not reached:** note detail/edit view, any error state, any help or documentation surface, mobile viewport
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect."
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | 02:41 (live preview only; no note ever saved) | at risk | Partial | Fail |
| power-user | not reached | not reached | Fail | Fail |

- Jargon density, Settings: 3 of 4 controls labelled in internal vocabulary; 1 ("Export — Markdown, all cards") plain.
- Jargon density, signup: 3 of 3 workspace-type options undefined on an irreversible choice.
- Naming: 1 concept, 3 words ("cards", "block", "notes") across 5 surfaces.

## Severity flips
- Workspace-type jargon: **P1 for novice** ("I don't know what any of these are"), shrugged off by power-user ("Fine — I've seen worse") — the signup copy is written for someone who already knows the category.
- Settings vocabulary: opaque to novice (P2, cannot read it at all) but a *consistency* problem for power-user (P2, cannot tell if it duplicates his signup choice) — two findings, not one.

## Next action
- Stop the two copy falsehoods first: no "Saved ✓" before the write is confirmed, and no "Memories" until one is derived from the user's own content.
