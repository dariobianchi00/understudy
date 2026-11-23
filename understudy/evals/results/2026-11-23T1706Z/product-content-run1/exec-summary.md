# Nimbus Notes — content — Run 2026-09-08 (fixture02)

Nimbus pitches "remembers everything so you never start from zero", then tells both personas "Saved ✓" for notes it loses and "remembers" facts about them that are false.

## Top 3
1. **[P0] "Saved ✓" confirms a note that never appears in "Your cards" or search** — both personas concluded the product lies; both gave up (novice, power-user)
2. **[P0] Memories page states three false facts about a novice who wrote one note** — her distrust spread to every confirmation: "is it making up the 'Saved' too?" (novice)
3. **[P1] Empty first screen contradicts the "never start from zero" promise for the novice** — she expected her stuff filled in, got "Nothing here yet." (novice)

## Score
- **Score:** 2/10 — the product's own words contradict its pitch and confirm saves that never happen; neither persona would return

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic persona mode); findings rest on personas the agent invented, not researched users
- **Not reached:** marketing site copy (promise taken from pre-session note only); the "Saved ✓" toast and "No results for '…'" copy are not visible in any screenshot — log evidence only
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect." Auth wall always excluded.
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | 02:41 (live preview only) | at risk | Partial | Fail |
| power-user | not reached | not reached | Partial | Fail |

- Jargon on screens the novice met: 6 infrastructure terms ("Federated graph", "Sovereign vault", "Hybrid mesh", "Enable webhook sync", "Federated graph replication", "Vault attestation")
- Names for one object: 3 ("cards", "block", "notes")
- Copy both personas called clear: "Markdown, all cards" export label

## Severity flips
- Memories false facts: P0 for novice (distrust spread to "Saved"), P1 for power-user (contained as "a demo panel")
- Empty dashboard: P1 for novice (arrived expecting auto-fill), non-issue for power-user ("Expected, nothing's in it yet")
- Signup workspace jargon: P2 for novice (guessed), non-issue for power-user ("I've seen worse")

## Next action
- Make the "Saved ✓" copy true — show the note in "Your cards" — then remove or source-label the Memories claims.
