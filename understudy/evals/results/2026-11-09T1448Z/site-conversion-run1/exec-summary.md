# Nimbus Notes — conversion — Run 2026-09-08 (fixture01)

Nobody can start a free trial on this site: every path ends at "Contact sales", and both personas left without taking any step.

## Top 3
1. **[P0] No free trial or self-serve signup exists; every call to action routes to sales** — the stated goal is unreachable from any page (evaluator, sceptic)
2. **[P0] Pricing page shows no price on any of its three plans** — the evaluator gave up and would look for an alternative (evaluator)
3. **[P1] Demo form requires five fields, including phone, before any product is shown** — the only offered path was abandoned unsubmitted (evaluator)

## Against the stated goal
**Goal:** Start a free trial without talking to sales
**Outcome:** could not — no trial path exists; would not, on both debriefs
**In their words:** "Nothing. I came to find out what it costs and I couldn't. I'd search for an alternative with a price on the page." (evaluator) · "Leave. The cookie bar and the privacy page disagree, and the privacy page won't say who the partners are." (sceptic)

## Score
- **Score:** 2/10 — no visitor can start a trial, no price is shown, and both personas left with no next step

## Limits on this read
- **Personas:** evaluator, sceptic — ⚠ INFERRED (generic); findings rest on personas the agent invented
- **Not reached:** sceptic never opened Pricing or the demo form; no form submitted (by design)
- **Excluded:** none in manifest; auth wall always
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | Forms opened / submitted | Price found | Scroll depth | Next step (Q3) |
|---|---|---|---|---|
| evaluator | 1 / 0 | No | 100% | Search for an alternative |
| sceptic | 0 / 0 | not sought | n/a | Leave |

- Severity count: P0 2 · P1 1 · P2 2 · P3 0
- Demo form: 7 fields, 5 required, phone required
- Calls to action leading to a trial: 0 of 5 crawled pages

## Severity flips
- None observed; the sceptic left for trust reasons before reaching the conversion surfaces.

## Next action
- Add a "Start free trial" button with an email-only signup to the hero and every pricing card, with a visible price.
