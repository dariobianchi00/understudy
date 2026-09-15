# Nimbus Notes — conversion — Run 2026-09-08 (fixture01)

The site offers no way to start a free trial at all — every route to the product ends at "Log in" or "Contact sales", so the stated goal is not hard here, it is absent, and the visitor who went looking for a price left to find a competitor.

## Top 3
1. **[P0] No self-serve trial exists: the only site-wide actions are Log in and Contact sales** — the goal the business named cannot be attempted on any page (evaluator, sceptic)
2. **[P0] Pricing page shows no price: all three plans say only Contact sales** — the evaluator's whole reason for visiting failed at 02:30 and she abandoned (evaluator)
3. **[P1] The newsletter band is the loudest call to action on the home page** — the only product action is a small outlined button beneath a full-width purple email capture (evaluator, sceptic)

## Against the stated goal
**Goal:** Start a free trial without talking to sales
**Outcome:** could not — no trial or sign-up affordance exists on any crawled page
**In their words:** "Nothing. I came to find out what it costs and I couldn't. I'd search for an alternative with a price on the page."

## Score
- **Score:** 2/10 — the named conversion goal is unreachable by construction, there is no price, and both visitors left without acting.

## Limits on this read
- **Personas:** evaluator (desktop 1440x900), sceptic (iPhone 13) — ⚠ INFERRED (`persona_mode: generic`); findings rest on personas the harness invented.
- **Not reached:** `/features.html` (404), anything behind `app/login.html`, any post-submission behaviour — no form was submitted, by design.
- **Excluded:** no scope exclusions declared; the auth wall is never scored.
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | Next step available at exit | Price found | Forms opened / submitted | Outcome |
|---|---|---|---|---|
| evaluator | none taken | No | 1 / 0 | Would not proceed — "no price" |
| sceptic | none taken | not sought | 0 / 0 | Left at 02:50 |

- Pages the evaluator reached with no onward action: `/about.html`, `/features.html` (404) — 2 of 5.
- CTA inventory on `/index.html`: 4 asks (Log in, "See it in action", newsletter Subscribe, "Request demo"); 0 of them start a trial.
- Demo form: 7 fields, 5 required, including a required phone number.

## Severity flips
- None observed on this lens. The sceptic never looked for a price, so the pricing P0 is scored on the evaluator alone rather than averaged across both.

## Next action
Add a "Start free trial" button to the header and to every pricing card, and put a number on at least the Starter plan.
