# Nimbus Notes — trust — Run 2026-09-08 (fixture01)

The About page convinced both personas Nimbus Notes is a real company, but a cookie banner contradicted by live tracking, a privacy page that names no one, and no price anywhere lost both of them.

## Top 3
1. **[P0] Cookie banner says "no tracking cookies" while a third-party analytics tracker loads and posts a visitor ID** — the site's first data promise is false on its own network log (evaluator, sceptic)
2. **[P1] Privacy page names no partners and no specifics, and the sceptic left over it** — the visitor who came for data answers walked away (sceptic)
3. **[P1] No plan shows a price, so the evaluator gave up on learning the cost** — the run's objective failed; "I'd search for an alternative" (evaluator)

## Score
- **Score:** 3/10 — both visitors believed the company exists, yet neither would trust it with money or data

> ⚠ **Personas are INFERRED (generic mode).** Findings rest on personas the agent invented, not researched ones.

## The four questions
| Question | Answered? | How long | What they concluded |
|---|---|---|---|
| Is this real? | partly | 03:50 (evaluator) · 01:30 (sceptic) | Company yes (About page); product never shown, testimonials disbelieved |
| What does it cost? | ✗ | gave up 02:30 (evaluator) · not sought (sceptic) | "Contact sales" on every plan; no number anywhere |
| Who is behind it? | ✓ | 03:50 (evaluator) · 01:30 (sceptic) | Named founder, Bristol address, company number — "a real company" |
| What happens to my data? | partly | 01:05 contradiction · 01:50 Frankfurt (sceptic) | Storage location found on About; sharing and tracking unanswered and contradicted |

## Objections raised
| Objection | Site's answer | Verdict |
|---|---|---|
| "no price, or a page that is all adjectives" | "Pricing depends on your workspace type and sync topology." | made worse |
| "I haven't seen the product and they want my phone number." | Phone field is `required` | made worse |
| "The cookie bar said no tracking. This page says they use cookies and share with partners. Which is it?" | Tracker fires on landing | made worse |
| "Nobody has a name. I don't believe these." | Nothing further | ignored |
| "Which partners? It doesn't say." | Nothing | ignored |
| "I want to see it 'remember' something." | "See it in action" does nothing | ignored |
| "who is behind this" (sceptic, pre-session) | Founder, address, company number on /about.html | answered |
| "what happens to my notes" (sceptic, pre-session) | "In the EU (Frankfurt) by default" — About only | partly |

## Limits on this read
- **Personas:** evaluator (desktop), sceptic (iPhone 13) — ⚠ INFERRED (generic)
- **Not reached:** sign-up / trial; sceptic never opened /pricing.html; demo form screenshot is blank
- **Excluded:** none in manifest; auth wall always excluded
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| evaluator | not reached | not reached | Fail | Partial |
| sceptic | not reached | not reached | Fail | Fail |

- Q5 outcome — evaluator: "Money, no … Data, unsure." · sceptic: "The privacy page took it back."
- Findings: 1 P0 · 3 P1 · 5 P2 · 0 P3

## Severity flips
- Vague privacy page: **P1 for the sceptic** (left over it) · **P2 for the evaluator** (noted it, left over price). The site answers the buyer's question worse than the privacy-minded visitor's.
- Pricing: no flip observable — the sceptic never looked for a price.

## Next action
- Remove or disclose the analytics tracker so the cookie banner is true, then rewrite /privacy.html to name every third party.
