# Nimbus Notes — ux — Run 2026-09-08 (fixture02)

Both personas wrote a note, were told "Saved ✓", found no trace of it in the list or in search, and quit inside seven minutes saying they would pay nothing.

## Top 3
1. **[P0] Save reports success but the note never appears in the cards list or search** — the one objective under test failed for both personas; both abandoned. (novice, power-user)
2. **[P0] Memories states three facts that are not the user's, and the novice stops trusting Save as a result** — a false claim about her own data made her doubt every other confirmation. (novice)
3. **[P2] Signup forces an irreversible workspace-type choice between three undefined terms** — the novice guessed on a decision the screen says cannot be undone. (novice)

## Score
- **Score:** 2/10 — neither persona could write a note and find it again, and both said no and nothing when asked whether they would return or pay.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic `persona_mode`); findings rest on personas the harness invented, not researched users.
- **Not reached:** note editing, note deletion, Cards surface with content, Export output, mobile or tablet viewports.
- **Excluded:** "The login wall at /app/login.html — infrastructure, not a defect."
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | 02:41 (live preview only; reversed at 03:12) | not reached — the note was lost 31s later | Fail | Fail |
| power-user | never | not reached — `first_value_reached: false` | Fail | Fail |

## Severity flips
- **Fabricated Memories:** P0 for the novice — it spread doubt to Save ("is it making up the 'Saved' too?"); P2 for the power-user, who shrugged it off as "a demo panel, I assume."
- **Irreversible workspace-type choice:** 28s of hesitation and a guess for the novice; "Fine — I've seen worse" for the power-user, who chose in seconds.
- **No keyboard shortcuts:** P2 for the power-user, who tested three; a non-issue for the novice, who never tried.
- **Reading:** the product is built for someone fluent in "federated graph" and "vault attestation", and says so nowhere.

## Next action
Make Save fail loudly when the write fails, and take the Memories panel down until it is built from the user's own notes.
