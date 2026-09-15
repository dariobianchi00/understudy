# Nimbus Notes — content — Run 2026-09-08 (fixture02)

Nimbus Notes tells the opposite story to its own pitch: it promises to "remember everything", then says "Saved ✓" to a note it loses and "remembers" three facts about the user that are not theirs.

## Top 3
1. **[P0] "Saved ✓" confirms a save the product did not perform** — both personas stopped believing anything the product said within 4 minutes (novice, power-user)
2. **[P0] "What Nimbus remembers about you" lists facts that are not the user's** — the surface carrying the whole pitch shows static, false second-person claims (novice; P1 for power-user)
3. **[P1] Product contradicts its pitch: "remembers everything" delivers an empty workspace and lost notes** — Q4 "No" from both personas; this is the root the other findings hang from (novice, power-user)

## Score
- **Score:** 2/10 — the product's own confirmations and its headline feature both state things that are false; the copy that is true is jargon.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic); findings rest on personas the run invented, not researched ones
- **Not reached:** the marketing site (promise taken from pre-session note only); "Cards" screen; Export output; any mobile viewport
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect."
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | 02:41 (live preview — persona's own call, weak) | healthy | Partial (Q2 reaches 2 of 3) | Fail |
| power-user | not reached | not reached | Partial (Q2 reaches 2, one broken) | Fail |

- Jargon: 7 undefined terms across 4 screens; 6 are infrastructure vocabulary ("Federated graph", "Sovereign vault", "Hybrid mesh", "webhook sync", "graph replication", "Vault attestation").
- Naming: the user's unit of writing is "notes", "cards" and "block" on one screen.
- Reading level: syntax trivial (≤ 8-word sentences); vocabulary is the barrier for the non-technical persona.

## Severity flips
- Memories panel: **P0 novice** ("is it making up the 'Saved' too?") vs **P1 power-user** ("a demo panel, I assume. Not going to trust it").
- Signup "workspace type" gate: **P1 novice** (guessed an irreversible choice) vs **P3 power-user** ("Fine — I've seen worse").
- Both flips point the same way: the copy was written for someone who already knows the architecture, and the pitch was written for someone who does not.

## Next action
- Stop "Saved ✓" firing until a card is actually listed, and replace the Memories sample rows with an honest empty state — both are copy-level changes that remove the two lies before any word of jargon is touched.
