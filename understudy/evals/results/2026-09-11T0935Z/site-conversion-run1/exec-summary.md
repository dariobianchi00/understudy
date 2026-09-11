# Nimbus Notes — conversion — Run 2026-09-08 (fixture01)

The stated goal is unreachable: the site offers no free trial anywhere, all three pricing plans route to the same seven-field sales form, and both personas ended the visit intending to do nothing.

## Top 3
1. **[P0] No self-serve trial exists — every route to the product ends at a sales form** — the one action the business wants is not on the site; the words "trial", "sign up" and "get started" appear zero times in the crawled HTML (evaluator, sceptic)
2. **[P0] Pricing lists three plans and no price** — the evaluator's whole reason for visiting went unanswered and she left to find a competitor with a number on the page (evaluator)
3. **[P1] The only form asks seven fields and requires a phone number before showing the product** — the sole conversion point demands a sales call's worth of data from a visitor who has seen nothing work (evaluator)

## Score
- **Score:** 2/10 — a visitor who wants to buy has no way to start; the only paths are "Log in", a newsletter, or handing a phone number to sales.

## Against the stated goal
**Goal:** Start a free trial without talking to sales
**Outcome:** could not tell → **would not**; no trial path exists to attempt, and both personas declined the sales path that replaced it
**In their words:** "Nothing. I came to find out what it costs and I couldn't. I'd search for an alternative with a price on the page."

## Limits on this read
- **Personas:** evaluator (desktop 1440x900), sceptic (iPhone 13) — ⚠ INFERRED (`persona_mode: generic`); findings rest on personas the capture invented, not researched ones
- **Not reached:** anything behind `app/login.html`; post-submission behaviour of the demo form (opened, never submitted, by design); `/features.html` (404)
- **Excluded:** none listed in `manifest.json`; the auth wall is never scored
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | Scroll depth | CTAs encountered | Forms opened / submitted | Price found | Next step taken |
|---|---|---|---|---|---|
| evaluator | 100% (4 sections) | 4 — "See it in action", newsletter, 3× "Contact sales", "Log in" | 1 / 0 | No | None — "I'd search for an alternative" |
| sceptic | 100% (1 section, straight to footer) | 2 — "See it in action", newsletter | 0 / 0 | No | None — "Leave." |

## Severity flips
- **Price absence:** P0 for the evaluator (came to price it, gave up at 02:30); not attempted by the sceptic, whose question was data handling. Not scored as a flip — one persona never tested it.

## Next action
Publish a currency price on the Starter and Team cards and put a self-serve "Start free trial" button beside each, replacing "Contact sales" everywhere except Enterprise.
