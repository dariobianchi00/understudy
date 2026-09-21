# Nimbus Notes — content — Run 2026-09-08 (fixture02)

Nimbus Notes tells both personas the opposite of what brought them here — it promised to remember everything, then showed them an empty workspace, told them a note was "Saved ✓" that it had not saved, and presented three confident facts about them that were not theirs.

## Top 3
1. **[P0] Memories page presents three facts about the user that are not theirs and claims they came from their notes** — the novice concluded the product invents things, then doubted the save confirmation too, and stopped. (novice)
2. **[P1] Entry promise "remembers everything so you never start from zero" appears nowhere in the product's own copy** — both personas answered Q4 "No"; neither could say what the product does for them. (novice, power-user)
3. **[P1] Failed save produces no error copy — "Saved ✓" and "Nothing here yet." are the only words offered** — both personas abandoned the one objective under test with no idea what had gone wrong. (novice, power-user)

## Score
- **Score:** 3/10 — the product's words actively misinform: two of two personas were told a note was saved when it was not, and shown "memories" that were not theirs.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic `persona_mode`); findings rest on personas the harness invented, not researched ones.
- **Not reached:** note-detail view, any populated list or populated search result, any error state other than zero-results.
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect."
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | 02:41 | healthy, then withdrawn — the saved note vanished | Fail — Q1 is "right now: nothing"; Q2 reached 2 | Fail |
| power-user | not reached | not reached — gave up at 03:00 | Fail — Q2 reached 2, "one of them doesn't work" | Fail |

- Jargon terms shipped in UI copy with zero explanation: **6** — "Federated graph", "Sovereign vault", "Hybrid mesh", "webhook sync", "Federated graph replication", "Vault attestation".
- Words used for one concept: **3** — "Cards", "block", "notes".

## Severity flips
- **Memories page.** P0 for the novice — "If it's making these up, is it making up the 'Saved' too?" — and P2 for the power-user, who wrote it off as "a demo panel, I assume" and carried on. Written as two findings (`e5ea569f5a58`, `025e866d7ecd`).
- **Signup jargon.** P2 for the novice, who guessed on an irreversible choice; a non-issue for the power-user — "Fine — I've seen worse." Not scored for the power-user.

## Next action
Stop the Memories page shipping fabricated statements under the heading "What Nimbus remembers about you" — it is the copy that cost this product the novice's trust in everything else it said.
