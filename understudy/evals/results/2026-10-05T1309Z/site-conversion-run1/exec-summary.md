# Nimbus Notes — conversion — Run 2026-09-08 (fixture01)

Nobody can start a free trial on this site, because none exists: every path ends at "Contact sales" and a seven-field demo form with a required phone number.

## Top 3
1. **[P0] No self-serve free trial exists anywhere; every plan routes to sales** — the stated goal is impossible on this site (evaluator)
2. **[P1] Pricing page shows no price on any of its three plans** — the evaluator gave up and would look for an alternative (evaluator)
3. **[P1] Contact sales lands on a seven-field demo form that requires a phone number** — the only conversion point; evaluator backed out (evaluator)

## Against the stated goal
**Goal:** Start a free trial without talking to sales
**Outcome:** would not — and could not: no trial path exists
**In their words:** "Nothing. I came to find out what it costs and I couldn't. I'd search for an alternative with a price on the page." (evaluator) · "Leave. The cookie bar and the privacy page disagree, and the privacy page won't say who the partners are." (sceptic)

## Score
- **Score:** 1/10 — the goal cannot be completed: no trial exists, and both visitors left without any next step

## Limits on this read
- **Personas:** evaluator, sceptic — ⚠ INFERRED (generic); findings rest on personas the agent invented
- **Not reached:** demo form on mobile; `/app/login.html`; any post-submission state (forms never submitted, by design)
- **Excluded:** none in manifest; auth wall always
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| evaluator | never (comprehension null) · left 06:30 | not reached | Fail | Partial |
| sceptic | never (comprehension null) · left 02:50 | not reached | Fail | Fail |

- Forms opened 1 · submitted 0 · price found 0 of 2
- Demo form: 7 fields, 5 required, phone among them

## Severity flips
- None observed. The sceptic left on trust grounds before reaching pricing, so the price and form findings rest on the evaluator alone.

## Next action
- Put a "Start free trial" self-serve signup on Starter and Team, with a price, and make it the home-page hero button.
