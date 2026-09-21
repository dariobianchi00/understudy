# Nimbus Notes — clarity — Run 2026-09-08 (fixture01)

Nobody understood what Nimbus Notes is from the site: both visitors answered "a notes app" from the brand name rather than the page, neither ever reached comprehension, and both left without it.

## Top 3
1. **[P0] Neither visitor could say what Nimbus Notes does from the page; both guessed from the brand name** — the site's one job above the fold went undone, and the whole session never repaired it (evaluator, sceptic)
2. **[P1] The fold's only call to action, "See it in action", does nothing when clicked** — the page's own answer to "what next" is `href="#"`, clicked by both visitors (evaluator, sceptic)
3. **[P2] The clearest description of the product is buried in the About FAQ, two clicks from the fold** — the sentence that would have explained everything arrived at 04:20, three minutes past the point of lost interest (evaluator, sceptic)

## Score
- **Score:** 3/10 — both visitors left unable to say what the product does from the page, and the fold's only next step is a dead link.

## Limits on this read
- **Personas:** evaluator (desktop 1440x900), sceptic (iPhone 13, 390x844) — ⚠ **INFERRED (generic)**; findings rest on personas the run invented, not researched ones
- **Not reached:** `/features.html` (404); pricing and features never seen on mobile; no tablet viewport; no returning-visitor state
- **Excluded:** none declared; the auth wall is never reported
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Comprehension
| Persona | What is it? | Who's it for? | What next? | Time to understand |
|---|---|---|---|---|
| evaluator | ✗ | ✗ | ✗ | never |
| sceptic | ✗ | ✗ | partly | never |

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| evaluator | never | not reached | Fail | Partial — "close but off" |
| sceptic | never | not reached | Fail | Fail — "No" |

- Time to comprehension: `null` for both personas; the benchmark window is 10–30 s.
- Point of lost interest: 01:25 (evaluator), 00:30 (sceptic).
- Session length: 6:30 (evaluator), 2:50 (sceptic, `left_early: true`).
- Unanswered questions logged: 5 (evaluator), 3 (sceptic).
- Undefined terms quoted by a persona: "bi-directional sync graph", "zero-knowledge vault", "workspace type", "sync topology", "blocks".
- Findings: 1 P0 · 1 P1 · 7 P2 · 1 P3.

## Severity flips
- **"What next" axis flips, the findings do not.** The sceptic recorded `understood_next_step: true` and the evaluator `false` — yet both clicked the same dead "See it in action", so the finding stays one P1 across both.
- Mobile-only: the clipped 390px fold is a finding for the sceptic and a non-issue for the evaluator at 1440px.

## Next action
Rewrite the hero to say, in plain words, that it is a notes app that syncs across devices and works offline — then point "See it in action" at something real.
