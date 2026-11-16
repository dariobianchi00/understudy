# Nimbus Notes — trust — Run 2026-09-08 (fixture01)

The About page convinced both visitors that Nimbus Notes is a real company, but neither would trust it with money or data: no price is shown, and the cookie bar's "no tracking cookies" claim is contradicted by the privacy page and by a tracker that fires on load.

> ⚠ **Generic personas.** `persona_mode: generic`, so these findings rest on two inferred personas, not researched ones.

## Top 3
1. **[P0] Cookie bar claims no tracking cookies while an analytics tracker fires before consent** — Both personas caught the contradiction, and it cancelled the trust the About page had built. (evaluator, sceptic)
2. **[P1] Pricing page shows no price on any plan, only Contact sales** — The evaluator gave up on price at 02:30 and would "search for an alternative". (evaluator)
3. **[P1] Privacy page names no partners and reserves unannounced changes** — The sceptic left at 02:40 because of it. It is P2 for the evaluator. (sceptic; evaluator at P2)

## Score
- **Score:** 3/10 — Both visitors believed the company exists, but neither would hand over money or data: no price, and a cookie claim the site contradicts.

## Limits on this read
- **Personas:** evaluator, sceptic — ⚠ INFERRED (generic)
- **Not reached:** the sceptic did not visit `/pricing.html`. The demo-form screenshot is blank. No cookie or storage inspection was done.
- **Excluded:** none in the manifest. The auth wall is never reported.
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## The four questions
| Question | Answered? | How long | What they concluded |
|---|---|---|---|
| Is this real? | partly | 03:50 (evaluator) · 01:30 (sceptic) | Real company, from About. The testimonials were disbelieved and no product was ever shown. |
| What does it cost? | ✗ | gave up 02:30 (evaluator) · not sought (sceptic) | Every plan says "Contact sales". "Money, no." |
| Who is behind it? | ✓ | 03:50 (evaluator) · 01:30 (sceptic) | Priya Raman, Bristol, company number 14482201. Both personas: "a real company". |
| What happens to my data? | partly | 01:50 (sceptic, Frankfurt) · never resolved | Storage location found on About. Partners unnamed, and cookie claims contradict each other. |

## Objections raised
| Objection | Site's answer | Verdict |
|---|---|---|
| "I can't find out what it costs. That's the thing I came to check." | Three "Contact sales" buttons and a seven-field form | made worse |
| "Nobody has a name. I don't believe these." | Nothing. All three quotes stay anonymous. | ignored |
| "I haven't seen the product and they want my phone number." | Phone is `required` | made worse |
| "Which partners? It doesn't say." | "We may share information with partners and service providers" | ignored |
| "The bar said no tracking cookies. This page says they use cookies. One of those is wrong." | A tracker loads and POSTs a uid on page load | made worse |
| "I want to see it "remember" something." | The "See it in action" button does nothing | ignored |
| "who is behind this" (sceptic pre-session) | About: named founder, address, company number | answered |
| "what happens to my notes" (sceptic pre-session) | About: "In the EU (Frankfurt) by default". The Privacy page does not say. | partly |

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| evaluator | not reached (price never found; left 06:30) | not reached | Fail | Partial |
| sceptic | not reached (left early 02:50) | not reached | Fail | Fail |

- Q5 outcome: evaluator "Money, no … Data, unsure". Sceptic: "The privacy page took it back."
- Findings: 1 P0 · 2 P1 · 5 P2 · 0 P3

## Severity flips
- Privacy page with unnamed partners: **P1 for the sceptic** (left because of it) and **P2 for the evaluator** (unsure, but left over price).
- No price: P1 for the evaluator. The sceptic never looked, so a flip could not be observed.

## Next action
- Make the cookie bar true: name the tracker and load it only after consent. Then publish a price on `/pricing.html`.
