# Nimbus Notes — bugs — Run 2026-09-08 (fixture02)

Saving a note fails silently behind a false "Saved ✓" toast, and the Memories panel fabricates personal facts neither persona ever gave it — both personas lost their work and left within seven minutes.

## Top 3
1. **[P0] Save reports success while the note is silently dropped** — `POST /api/notes` 500s every time; the note vanishes and the UI lies that it saved (novice, power-user)
2. **[P1] Memories panel presents fabricated personal facts as real** — invents habits, tools and projects for accounts with zero saved notes, destroying trust in every other signal the product gives (novice, power-user)
3. **[P2] Uncaught ReferenceError floods console on every dashboard load** — `renderGraphOverlay is not defined` fires on every dashboard visit; likely masking a missing feature (novice, power-user)

## Score
- **Score:** 2/10 — the one thing this product must do, keep a note, fails every time and tells the user it worked.

## Limits on this read
- **Personas:** novice, power-user — ⚠ INFERRED (generic)
- **Not reached:** multi-note organization, search over real data, Export button behavior, mobile/tablet viewports
- **Excluded:** The login wall at /app/login.html — infrastructure, not a defect.
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| novice | not reached (161s attempt, save failed) | at risk | Fail | Fail |
| power-user | not reached (save failed) | at risk | Fail | Fail |

## Severity flips
- None — the save failure (P0) and Memories fabrication (P1) hit both personas identically; no flip observed.

## Next action
Fix the `/api/notes` 500 and stop the UI from claiming success on failure before anything else ships.
