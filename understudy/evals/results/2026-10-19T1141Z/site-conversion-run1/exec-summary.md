# Nimbus Notes — conversion — Run 2026-09-08 (fixture01)

Nimbus Notes has no way to start a free trial: every call to action leads to a sales form, and one does nothing, so the evaluator left to look for an alternative.

> ⚠ **Personas are INFERRED (generic).** Both personas were invented for this run, not researched, so treat every finding as weaker than it would be with real audience evidence.

## Top 3
1. **[P0] No free-trial path exists on any page; every route to the product ends at sales** — the stated goal cannot be reached by anyone, whatever they think of the product (evaluator)
2. **[P1] Pricing page shows no price on any plan, so the visitor cannot judge the trial is worth starting** — the evaluator gave up at 02:30 and named this as why they would leave (evaluator)
3. **[P1] The only form asks for 5 required fields including phone before any product is shown** — the evaluator counted the fields and backed out at 03:15 (evaluator)

## Against the stated goal
**Goal:** Start a free trial without talking to sales
**Outcome:** would not
**In their words:** "Nothing. I came to find out what it costs and I couldn't. I'd search for an alternative with a price on the page."

- Evaluator: would not. Sought a price, found "Contact sales" ×3, backed out of the demo form, ended at "search for an alternative".
- Sceptic: would not. Q3: "Leave." Left for trust reasons at 02:40 and never looked for a trial.
- Neither persona *could* have succeeded: the crawled site has no trial, sign-up or "get started" link (`crawl/html/*.html`).

## Score
- **Score:** 2/10 — no visitor can start a trial without talking to sales; the one persona who tried to act left for an alternative.

## Limits on this read
- **Personas:** evaluator (desktop 1440×900), sceptic (iPhone 13) — ⚠ INFERRED (generic)
- **Not reached:** the demo form's submitted state (not submitted, by design) · `app/login.html` (auth wall, not scored) · `/features.html` returned 404
- **Excluded:** none in scope exclusions · auth wall always excluded
- **Models:** traversal `fixture-hand-authored` · scoring `opus`
- **Evidence gap:** `persona-evaluator/screenshots/03-demo-form.png` is blank. Form fields were counted from the crawled DOM and the partial view in `01-scrolled.png`

## Numbers
| Persona | Goal reached | Price found | Forms opened / submitted | Scroll depth | Session | Q3 outcome |
|---|---|---|---|---|---|---|
| evaluator | No | No | 1 / 0 | 100% | 6:30 | "search for an alternative" |
| sceptic | No | Not sought | 0 / 0 | 100% | 2:50 (left early) | "Leave." |

- Calls to action on the landing page: 4 (Log in, See it in action, Subscribe, Request demo). Trial: 0.
- Pricing CTAs: 3, all "Contact sales", all pointing to `index.html#demo`.
- Demo form: 7 fields, 5 marked `required`. Phone is one of the 5.

## Severity flips
- None scored as a flip. The sceptic never reached the conversion path. Their exit was driven by privacy and cookie copy, which belongs to the trust lens, so no conversion severity could be observed for them.

## Next action
- Add a "Start free trial" button as the filled primary action in the hero, the nav and each pricing card, and point it at a self-serve sign-up page instead of `#demo`.
