# Nimbus Notes — trust — Run 2026-09-08 (fixture01)

Both visitors found a real company on the About page and then lost that trust on the Privacy page, because the cookie bar's "no tracking cookies" promise is contradicted by the policy text and by a tracker that fires on first load.

## Top 3
1. **[P0] Cookie bar promises no tracking cookies; a third-party tracker fires on load and the privacy page says otherwise** — the one explicit data promise the site makes is false on the evidence, and both visitors caught it (evaluator, sceptic)
2. **[P1] Pricing page shows no price on any plan and explains it with jargon the visitor cannot answer** — the evaluator's "would you trust them with your money" is a flat no; she left to find a competitor with a price (evaluator)
3. **[P1] Privacy page names no partners, no data categories and no cookie behaviour** — the sceptic's whole visit was this question; the page's answer was "Use the demo form", and he left (evaluator, sceptic)

## Score
- **Score:** 3/10 — provenance is good (named founder, address, company number, EU data location) but pricing is absent, proof is anonymous, and the site's own cookie promise is contradicted by its network traffic.

## The four questions
| Question | Answered? | How long | What they concluded |
|---|---|---|---|
| Is this real? | partly | 03:50 (evaluator) · 01:30 (sceptic) | A real company, yes; a real product, never seen — the only demo button does nothing |
| What does it cost? | ✗ | gave up at 02:30 (evaluator); sceptic did not ask | "Every one says 'Contact sales'. No numbers anywhere." |
| Who is behind it? | ✓ | 03:50 (evaluator) · 01:30 (sceptic) | "Priya Raman, Bristol, 2023, company number 14482201, eight people. Good. That is a real company." |
| What happens to my data? | ✗ | 05:20 (evaluator) · 01:05 (sceptic) | Cookie bar and privacy page disagree; partners unnamed; the real answer (Frankfurt) is on About |

## Objections raised
| Objection | Site's answer | Verdict |
|---|---|---|
| "The bar said no tracking cookies. This page says they use cookies. One of those is wrong." | Nothing — and `network-full.txt` shows `analytics.example-tracker.test` firing on load | made worse |
| "I don't know what my workspace type is. I haven't got one." | "Pricing depends on your workspace type and sync topology." — no definition anywhere | made worse |
| "'Share with partners' — which partners? Not said." | "Questions? Use the demo form." | ignored |
| "Three quotes, nobody has a name. I don't believe these." | Nothing | ignored |
| "Seven fields. Phone required. I haven't seen the product." | Nothing | ignored |
| "I want to see it 'remember' something. The button does nothing when I tap it." | Nothing | ignored |
| "who is behind this" (sceptic pre-session) | About: named founder, address, company number, headcount, founding year | answered |

## What raised trust
- About page: "Nimbus Notes Ltd", "eight people", "2023", "Priya Raman", "14 Harbourside Walk, Bristol", "Company number 14482201" — both personas' first `trust_up`.
- About FAQ: offline works, Markdown export "on every plan", data "In the EU (Frankfurt) by default" — the sceptic called it "the answer I wanted".

## Limits on this read
- **Personas:** evaluator (desktop 1440×900), sceptic (iPhone 13) — ⚠ INFERRED (generic). Findings rest on personas the run invented, not researched ones.
- **Not reached:** /features.html (404 for the evaluator; sceptic never tried) · pricing and testimonials never seen by the sceptic (left at 02:50).
- **Excluded:** none in manifest — auth wall never reported.
- **Models:** traversal `fixture-hand-authored` · scoring `opus`.
- **Evidence gap:** `persona-evaluator/screenshots/01-scrolled.png` and `03-demo-form.png` are blank captures; testimonial and demo-form findings rest on `session.log` and `findings-raw.json` only.
- Not a compliance review; nothing here says whether the privacy policy is legally sufficient.

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| evaluator | null (never understood what it is) | at risk — lost interest 01:25 | Fail | Partial — "close but off" |
| sceptic | null | not reached — left 02:50 | Fail | Fail — "No" |

- Q5 outcome: evaluator "Money, no … Data, unsure"; sceptic "The About page made them real … The privacy page took it back."
- `price_found: false` for both; `forms_submitted: 0`.

## Severity flips
- None observed. The sceptic never opened Pricing or scrolled to the testimonials, so whether those flip for a sceptic could not be tested. The cookie/privacy contradiction landed identically on both.

## Next action
Make the cookie bar true or remove it: either drop `analytics.example-tracker.test` from first load, or change the bar and the privacy page to say what is actually set and who receives it.
