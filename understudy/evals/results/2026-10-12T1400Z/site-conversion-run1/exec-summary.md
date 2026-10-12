# Nimbus Notes — conversion — Run 2026-09-08 (fixture01)

No visitor can start a free trial because the site has no trial path at all — every route ends at "Contact sales" or a phone-required demo form.

> ⚠ **Persona mode: generic.** Both personas were inferred, not researched; weigh every finding accordingly.

## Top 3
1. **[P0] No free-trial path exists; every route to sign-up ends at sales or a demo form** — the stated goal is unreachable for every visitor (evaluator, sceptic)
2. **[P1] Pricing page shows no prices and sends all three plans, including the individual tier, to sales** — the evaluator gave up and would look for an alternative (evaluator)
3. **[P1] Demo form demands five required fields, including phone, before any product is shown** — the only form on the site was opened and abandoned (evaluator)

## Against the stated goal
**Goal:** Start a free trial without talking to sales
**Outcome:** could not — no trial action exists on any of the 5 pages crawled
**In their words:** "Nothing. I came to find out what it costs and I couldn't. I'd search for an alternative with a price on the page."

## Score
- **Score:** 2/10 — neither visitor could start a trial; the only offered step was talking to sales, the exact thing the goal rules out

## Limits on this read
- **Personas:** evaluator (desktop), sceptic (iPhone 13) — ⚠ INFERRED (generic)
- **Not reached:** `app/login.html`; sceptic never saw pricing or the demo form; no form submitted
- **Excluded:** none in manifest · auth wall always
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | Reached goal | Price found | Forms opened / submitted | Pages with no onward step | Debrief Q3 |
|---|---|---|---|---|---|
| evaluator | No | No | 1 / 0 | 2 of 5 (About, Features 404) | "Nothing" |
| sceptic | No | Not sought | 0 / 0 | 1 of 2 (About) | "Leave" |

- Demo form: 7 controls, 5 required, phone required (counted from markup; screenshot blank)
- Calls to action on home, by visual weight: newsletter → "Log in" → "See it in action" (inert) → "Request demo"
- Severity count: P0 1 · P1 2 · P2 2 · P3 0

## Severity flips
- None observed; the sceptic left on trust grounds before reaching pricing or the form, so the P1s were not tested on her.

## Next action
- Ship a self-serve "Start free trial" button in the hero, header and Starter/Team pricing cards; size of the lift is untested.
