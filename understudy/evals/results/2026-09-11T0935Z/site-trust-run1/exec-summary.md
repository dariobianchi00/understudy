# Nimbus Notes — trust — Run 2026-09-08 (fixture01)

Both visitors finished believing Nimbus Notes is a real company and unwilling to hand it money or data, because the cookie bar's "no tracking cookies" promise is contradicted by the page's own tracker, the privacy page names no partners, and no plan carries a price.

## Top 3
1. **[P0] Cookie bar claims no tracking cookies while a third-party tracker loads and posts a user id** — the one verifiable promise on the site is false on the same page load. (evaluator, sceptic)
2. **[P1] Privacy page names no partners, and the sceptic left over it** — she abandoned at 02:40 with "data handling unclear". (sceptic)
3. **[P1] No price anywhere; three plans all say "Contact sales"** — the evaluator gave up at 02:30 and said he would search for an alternative. (evaluator)

## The four questions
| Question | Answered? | How long | What they concluded |
|---|---|---|---|
| Is this real? | partly | 01:30 (sceptic) · 03:50 (evaluator) | The company is real; the product and its customers are not shown. |
| What does it cost? | ✗ | 02:30 (evaluator gave up) | "I came to find out what it costs and I couldn't." |
| Who is behind it? | ✓ | 01:30 (sceptic) · 03:50 (evaluator) | Priya Raman, Bristol, company number 14482201, eight people, founded 2023. |
| What happens to my data? | ✗ | 01:05 (sceptic) · 05:20 (evaluator) | Partners unnamed, cookie claim contradicted; only the storage location is stated. |

## Objections raised
| Objection | Site's answer | Verdict |
|---|---|---|
| "Three quotes, nobody has a name. I don't believe these." | Nothing — no named customer anywhere on the site | ignored |
| "'Share with partners' — which partners? Not said." | "We may share information with partners and service providers" | ignored |
| "The bar said no tracking cookies. This page says they use cookies." | Neither surface reconciles the other | made worse |
| "I don't know what my workspace type is. I haven't got one." | "Pricing depends on your workspace type and sync topology." | made worse |
| "I haven't seen the product and they want my phone number." | Phone is a required field on the only route to a price | made worse |
| "I want to see it 'remember' something. The button does nothing when I tap it." | "See it in action" links to `#` | made worse |
| "Where is my data stored?" | About page: "In the EU (Frankfurt) by default." | answered |

## Score
- **Score:** 4/10 — strong provenance (named founder, address, company number) sits under a cookie promise the page itself breaks, an empty privacy page and no price, so neither visitor would commit money or data.

## Limits on this read
- **Personas:** evaluator (desktop 1440x900), sceptic (iPhone 13) — ⚠ INFERRED (`persona_mode: generic`); findings rest on personas the harness invented.
- **Not reached:** `/features.html` (404), the logged-in app, any product screen or demo.
- **Excluded:** none declared in `manifest.json`; the auth wall is never reported.
- **Models:** traversal `fixture-hand-authored` · scoring `opus`
- **Scope:** what the site said, only. No company register, news or outside knowledge was consulted; every absence below is "the site does not say", never "the company does not".

## Numbers
| Persona | Session | Price found | Q5 — money | Q5 — data | Trust_up / trust_down |
|---|---|---|---|---|---|
| evaluator | 6:30 | no (gave up 02:30) | No | Unsure | 2 / 4 |
| sceptic | 2:54, left early | not sought | not stated | No — "the privacy page took it back" | 2 / 3 |

## Severity flips
- **The vague privacy page flips P1 → P2.** It ended the sceptic's visit at 02:40; the evaluator saw the same page at 05:20, called it a contradiction, and kept reading. A visitor who leads with the data question leaves; one who leads with price never gets there.
- **Price is P1 for the evaluator and unobserved for the sceptic** — she never looked, so this is a gap, not a non-issue.

## Next action
Make the cookie bar true — either remove `analytics.example-tracker.test` from the home page or replace the "no tracking cookies" claim with a consent choice — then put a number on the Starter plan.
