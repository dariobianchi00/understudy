# Nimbus Notes — content — Run 2026-09-08 (fixture02)

The product's words claim the "remembers everything" pitch ("Saved ✓", "What Nimbus remembers about you"), the product does neither, and both personas quit saying it does nothing for them.

## Top 3
1. **[P0] "Saved ✓" confirms a save that failed, and no error copy is ever shown** — every note both personas wrote was lost while the UI said it was safe (novice, power-user)
2. **[P0] Memories presents three invented facts as "What Nimbus remembers about you"** — novice concluded "Saved" was probably made up too; power-user dismissed it as "a demo panel" (P1) (novice, power-user)
3. **[P1] "Never start from zero" pitch meets a blank "Nothing here yet." dashboard** — the novice came expecting her stuff and found nothing, and said so in Q4 (novice)

## Score
- **Score:** 2/10 — the copy promises memory and confirms saves that never happened; both personas quit and would pay nothing

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic). Findings rest on personas the agent invented, not researched users
- **Not reached:** marketing site copy (promise known only from the pre-session line); any error state; mobile
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect."
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Promise vs delivery
| Persona | Arrived expecting | Product delivered | Match |
|---|---|---|---|
| novice | "remembers everything so you never start from zero" → "fills itself in from things I already have" | Empty dashboard, lost notes, false memories | Fail |
| power-user | same promise → "fast capture, good search, keyboard-driven" | Save stores nothing, search finds nothing, memories "Not me" | Fail |

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | 02:41 (live word count/preview only) | healthy by clock; value never kept | Fail | Fail |
| power-user | not reached | not reached | Fail | Fail |

- Jargon: 6 unexplained terms across signup and Settings ("Federated graph", "Sovereign vault", "Hybrid mesh", "Enable webhook sync", "Federated graph replication", "Vault attestation")
- Naming: one object, three nouns — "cards", "block", "notes"
- Findings: 2 P0 · 2 P1 · 5 P2 · 1 P3

## Severity flips
- Memories false facts: P0 for novice (trust collapsed) · P1 for power-user (written off as a demo)
- Empty start vs "never start from zero": P1 for novice · non-issue for power-user ("Expected, nothing's in it yet")
- Signup workspace jargon: P2 for novice (guessed an irreversible choice) · P3 for power-user ("I've seen worse")
- The product's copy is written for the power-user's vocabulary while its pitch targets the novice

## Next action
- Make "Saved ✓" appear only on a confirmed save, and remove the sample Memories, before touching any other copy.
