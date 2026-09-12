# Nimbus Notes — conversion — Run 2026-09-08 (fixture01)

The site cannot convert against its own goal: there is no free-trial path anywhere, no price on any plan, and the only visitor who went looking left to search for an alternative.

## Against the stated goal
**Goal:** Start a free trial without talking to sales
**Outcome:** could not tell — no trial entry point exists; every action routes to sales or log-in
**In their words:** "Nothing. I came to find out what it costs and I couldn't. I'd search for an alternative with a price on the page." (evaluator) · "Leave. The cookie bar and the privacy page disagree, and the privacy page won't say who the partners are." (sceptic)

## Top 3
1. **[P0] No self-serve trial path exists: every call to action routes to sales or log-in** — the stated goal is unreachable by any route on the site (evaluator, sceptic)
2. **[P0] Pricing page shows no price on any of its three plans** — the evaluator's stated reason for leaving; the run objective "find the cost without giving an email" failed (evaluator)
3. **[P1] Demo form demands 7 fields, 5 required including phone, before any product is shown** — the only route off the Pricing page, and the evaluator backed out at 03:15 (evaluator)

## Score
- **Score:** 2/10 — a trial cannot be started, a price cannot be found, and the one above-the-fold action does nothing; conversion mostly fails

## Limits on this read
- **Personas:** evaluator (desktop 1440×900), sceptic (iPhone 13) — ⚠ INFERRED (generic); findings rest on personas the run invented, not researched ones
- **Not reached:** `app/login.html` (not clicked); `/features.html` content (404); no form submitted by design
- **Excluded:** none in manifest — auth wall always
- **Models:** traversal `fixture-hand-authored` · scoring `opus`
- **Evidence gap:** `persona-evaluator/screenshots/03-demo-form.png` captured blank; form field count taken from `crawl/html/1-index.html:29-34` and `session.log:21`

## Numbers
| Persona | Goal attempted | Price found | Forms opened / submitted | Session | Q3 outcome |
|---|---|---|---|---|---|
| evaluator | yes — 01:48 to 02:30, gave up | no | 1 / 0 | 6:30, full scroll | would not proceed |
| sceptic | no — question was data handling | not sought | 0 / 0 | 2:50, left early | would not proceed |

- CTAs on the home page, by visual weight: 1 newsletter band (full-width solid purple) · 2 "Log in" (filled nav button) · 3 "See it in action" (small outlined, `href="#"`)
- Calls to action leading to a trial or signup: 0 across 5 pages
- "Contact sales" buttons: 3, all linking to `index.html#demo`
- Dead-end pages reached (no onward action): 3 — `/about.html`, `/privacy.html`, `/features.html` (404)

## Severity flips
- None observable: the sceptic never attempted the goal, so the pricing and form findings are evaluator-only by design, not a flip
- Both personas hit the inert hero button at the same severity

## Next action
Put a price and a "Start free trial" button on all three pricing cards, and make the hero button link to it — size of the effect is untested, but today the goal has no route at all.
