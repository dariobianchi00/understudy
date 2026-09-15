# Nimbus Notes — clarity — Run 2026-09-08 (fixture01)

Neither visitor ever learned what Nimbus Notes does: both answered "a notes app" from the brand name rather than the page, and `time_to_comprehension_seconds` is `null` for both.

## Top 3
1. **[P0] Neither persona could say what Nimbus Notes does; both answered from the brand name** — 100% comprehension failure in 6:30 and 2:50 of looking. (evaluator, sceptic)
2. **[P1] The only sentence describing the product uses three terms the visitor could not define** — "bi-directional sync graph", "zero-knowledge vault" replace the explanation instead of being it. (evaluator, sceptic)
3. **[P1] The clearest plain-English description of the product is two clicks away on the About page** — the sentence that would have worked is on a page most visitors never open. (evaluator, sceptic)

## Score
- **Score:** 3/10 — two visitors, two devices, two full sessions, and zero correct answers to "what is this".

## Comprehension
| Persona | What is it? | Who's it for? | What next? | Time to understand |
|---|---|---|---|---|
| evaluator | ✗ | ✗ | ✗ | never |
| sceptic | ✗ | ✗ | ✓ | never |

## Limits on this read
- **Personas:** evaluator (desktop 1440×900), sceptic (iPhone 13) — ⚠ INFERRED (generic `persona_mode`); findings rest on personas the run invented.
- **Not reached:** `/features.html` (404 on the nav link); logged-in app.
- **Excluded:** none declared in `manifest.json`; the auth wall is never reported.
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| evaluator | never | at risk (lost interest 01:25) | Fail | Partial |
| sceptic | never | at risk (lost interest 00:30) | Fail | Fail |

- Questions the site never answered: 5 (evaluator), 3 (sceptic).
- Undefined terms collected: 4 — "bi-directional sync graph", "zero-knowledge vault", "workspace type", "sync topology".
- Scroll depth: 100% both. Comprehension did not improve with depth.

## Severity flips
- **"What do they want me to do?"** — evaluator `understood_next_step: false`, sceptic `true` at the same fold; the sceptic accepted "See it in action", the evaluator read the brighter newsletter box as the real ask. Scored against the evaluator only, in `07d6fd69bdaa`.

## Next action
Replace the hero subhead with the About page's own sentence — "stores every note on your device first and syncs when a connection returns" — and name the audience above the fold.
