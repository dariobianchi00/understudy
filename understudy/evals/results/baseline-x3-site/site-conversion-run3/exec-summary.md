# Nimbus Notes — conversion — Run 2026-09-08 (fixture01)

The site offers no way to start a free trial anywhere, so the stated goal is unreachable and both visitors left without a next step.

## Against the stated goal
**Goal:** Start a free trial without talking to sales
**Outcome:** could not tell — no trial path exists to reach; every product path ends at "Contact sales" or a 7-field demo form
**In their words:** "Nothing. I came to find out what it costs and I couldn't. I'd search for an alternative with a price on the page." (evaluator) · "Leave. The cookie bar and the privacy page disagree, and the privacy page won't say who the partners are." (sceptic)

## Top 3
1. **[P0] No self-serve trial exists; every path to the product ends at Contact sales** — the goal cannot be taken by anyone; the only account link is "Log in" for existing users (evaluator, sceptic)
2. **[P1] Pricing page shows no numbers, so the visitor cannot work out what they would pay** — the visitor who came to check the price gave up at 02:30 and went to search for an alternative (evaluator)
3. **[P1] The only above-fold call to action goes nowhere, leaving the fold with no next step** — "See it in action" is `href="#"`; both visitors clicked it and nothing happened (evaluator, sceptic)

## Score
- **Score:** 2/10 — no trial, no price, a dead hero button and a phone-required demo form; the site cannot convert the visitor the goal describes

## Limits on this read
- **Personas:** evaluator (desktop-1440x900), sceptic (iphone-13) — ⚠ INFERRED (generic)
- **Not reached:** `app/login.html`; `/features.html` (404); pricing and demo form on mobile; `03-demo-form.png` captured blank, form judged from served markup and session log
- **Excluded:** none in manifest — auth wall always
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| evaluator | null (never understood the offer) | at risk — interest lost 01:25, left 06:30 | Fail | Partial ("close but off") |
| sceptic | null (never understood the offer) | not reached — 1 section, left early 02:50 | Fail | Fail ("no") |

- Forms opened / submitted: evaluator 1 / 0 · sceptic 0 / 0
- Price found: evaluator no · sceptic did not look
- Demo form: 7 fields, 5 required, phone required — counted from `crawl/html/1-index.html:30-33`

## Severity flips
- None observed. The price finding hits the evaluator only because the sceptic never sought a price; that is a coverage gap, not a flip.

## Next action
Add a "Start free trial" button to the hero and the Starter/Team pricing cards, pointing at an email-and-password signup, and print a price on those cards — the size of the gain is untested, but today the goal converts at zero.
