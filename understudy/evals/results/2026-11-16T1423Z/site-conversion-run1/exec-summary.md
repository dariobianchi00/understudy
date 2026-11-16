# Nimbus Notes — conversion — Run 2026-09-08 (fixture01)

Nobody can start a free trial without talking to sales, because the site offers no trial at all — every route ends at a seven-field "Contact sales" demo form.

## Top 3
1. **[P0] No free-trial or sign-up action exists anywhere; every plan routes to Contact sales** — the stated goal cannot be completed by any visitor (evaluator)
2. **[P1] No plan shows a price, so the evaluator gave up and would look for an alternative** — the cost-checker left for a competitor search (evaluator)
3. **[P1] Contact sales leads to a seven-field demo form that requires a phone number before any product is shown** — 5 required fields before any value; the form was opened and abandoned (evaluator)

## Against the stated goal
**Goal:** Start a free trial without talking to sales
**Outcome:** would not
**In their words:** "Nothing. I came to find out what it costs and I couldn't. I'd search for an alternative with a price on the page."
- No trial path exists, so "reached" was impossible for any persona
- Sceptic's Q3: "Leave." — left at 02:40 on trust grounds, before any ask

## Score
- **Score:** 1/10 — the goal is structurally unreachable: no trial exists, no price is shown, and the only ask is a sales form

## Limits on this read
- **Personas:** evaluator (desktop 1440×900), sceptic (iPhone 13) — ⚠ INFERRED (generic); findings rest on invented personas
- **Not reached:** any trial or sign-up flow (none exists); sceptic never opened pricing or a form
- **Excluded:** none in `scope_exclusions`; auth wall (`app/login.html`) always excluded
- **Models:** traversal `fixture-hand-authored` · scoring `opus`
- `03-demo-form.png` is blank; demo form scored from DOM

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| evaluator | not reached | not reached | Fail | Partial |
| sceptic | not reached | not reached | Fail | Fail |

- Asks on the site toward the goal: 0 · sales asks: 4 ("Contact sales" ×3, "Request demo")
- Demo form: 7 fields, 5 required, phone required · forms opened 1, submitted 0
- Prices shown: 0 of 3 plans

## Severity flips
- None — the sceptic left before reaching any ask, so the trial and pricing findings could not be tested on them.

## Next action
- Put a "Start free trial" button, with a visible price, on Starter and Team and as the solid hero button.
