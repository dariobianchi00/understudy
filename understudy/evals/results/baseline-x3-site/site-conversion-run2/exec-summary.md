# Nimbus Notes — conversion — Run 2026-09-08 (fixture01)

The site cannot convert on its stated goal because no free-trial path exists on any page — every plan ends in "Contact sales", the hero button goes nowhere, and both visitors left having done nothing.

## Against the stated goal
**Goal:** Start a free trial without talking to sales
**Outcome:** could not tell — no trial route exists for a visitor to reach
**In their words:** "Nothing. I came to find out what it costs and I couldn't. I'd search for an alternative with a price on the page." (evaluator) · "Leave. The cookie bar and the privacy page disagree, and the privacy page won't say who the partners are." (sceptic)

## Top 3
1. **[P0] No free-trial path exists on any page; the only action on every plan is "Contact sales"** — the goal is unreachable by design, not by friction (evaluator)
2. **[P1] Hero button "See it in action" links to "#" and does nothing when clicked** — the only above-fold next step is inert on desktop and mobile (evaluator, sceptic)
3. **[P1] No plan shows a price, so the evaluator could not decide and left to find an alternative** — the visitor who came to check cost gave up at 02:30 (evaluator)

## Score
- **Score:** 2/10 — a visitor who wants a self-serve trial has no button to press; the routes that exist (demo form, 7 fields, phone required) point at sales

## Limits on this read
- **Personas:** evaluator (desktop 1440×900), sceptic (iPhone 13) — ⚠ INFERRED (generic)
- **Not reached:** "Log in" (`app/login.html`); Pricing and demo form not opened by sceptic; nothing after form submission (by design)
- **Excluded:** none listed in manifest — auth wall always
- **Models:** traversal `fixture-hand-authored` · scoring `opus`
- **Evidence caveat:** `03-demo-form.png` captured blank; form fields counted from captured DOM (`crawl/html/1-index.html:29-34`)

## Numbers
| Persona | Pages reached | Next step available at exit | Forms opened / submitted | Price found | Q3 outcome |
|---|---|---|---|---|---|
| evaluator | 5 (+1 404) | No — home page, no working CTA | 1 / 0 | No | "Nothing" — would search for an alternative |
| sceptic | 3 | No — home page, dead button | 0 / 0 | Not sought | "Leave" |

- Calls to action found, by visual weight: newsletter (solid block) > "Log in" (nav) > "See it in action" (outlined, dead) > "Contact sales" ×3 > "Request demo"
- Trial / signup buttons on the site: 0
- Demo form: 7 fields, 5 required, phone required
- Dead-end pages reached: `/features.html` (404), `/about.html`, `/privacy.html`

## Severity flips
- None observed. The dead hero button and the newsletter hierarchy landed at the same severity for both personas.
- Price absence and form burden are evaluator-only: the sceptic never opened Pricing, so a flip could not be observed.

## Next action
Add a "Start free trial" button — solid purple, in the hero and on the Starter and Team cards — linking to an email-only signup; the size of the lift is untested, but today the number of trials this site can start is zero.
