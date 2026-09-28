# Nimbus Notes — conversion — Run 2026-09-08 (fixture01)

No visitor can start a free trial without talking to sales, because no self-serve trial exists and every pricing card ends in "Contact sales".

## Top 3
1. **[P0] No self-serve free trial exists anywhere on the site** — the stated goal cannot be reached by anyone (evaluator, sceptic)
2. **[P1] Pricing page shows no prices; all three plans route to Contact sales** — the evaluator gave up here and would search for an alternative (evaluator)
3. **[P1] Demo form demands 7 fields, 5 required including phone, before any product is shown** — the only route forward was abandoned unfilled (evaluator)

## Against the stated goal
**Goal:** Start a free trial without talking to sales
**Outcome:** could not. No trial path exists; neither persona would have gone further
**In their words:** "Nothing. I came to find out what it costs and I couldn't. I'd search for an alternative with a price on the page." (evaluator) · "Leave. The cookie bar and the privacy page disagree, and the privacy page won't say who the partners are." (sceptic)

## Score
- **Score:** 2/10 — The goal cannot be completed. The only way in is a sales form, and neither visitor would take a next step.

## Limits on this read
- **Personas:** evaluator, sceptic — ⚠ INFERRED (generic). These findings rest on personas the agent invented, not researched ones
- **Not reached:** `/app/login.html`. The sceptic opened no form and never looked at pricing
- **Excluded:** none in the manifest. The auth wall is always excluded
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | Scroll depth | Forms opened / submitted | Price found | Next step (Q3) |
|---|---|---|---|---|
| evaluator | 100% | 1 / 0 | No | None; would search for an alternative |
| sceptic | 100% | 0 / 0 | Not sought | Leave |

- Findings: 1 P0 · 2 P1 · 2 P2 · 0 P3
- Actions on the site: 7 (hero, newsletter, demo form, 3× "Contact sales", "Log in"). None of them starts a trial

## Severity flips
- None observed. The sceptic left over trust before reaching pricing or any form, so the P1s rest on the evaluator alone.

## Next action
- Ship a self-serve "Start free trial" button in the hero, the nav and the Starter and Team cards, with prices shown. How much this lifts conversion is untested.
