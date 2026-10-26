# Nimbus Notes — trust — Run 2026-09-08 (fixture01)

Both visitors left without trusting Nimbus Notes: the About page convinced them a real company exists, but a "no tracking cookies" banner the network log contradicts, a vague privacy page, and no price anywhere took that back.

> ⚠ **Personas are INFERRED (`persona_mode: generic`).** Findings rest on personas the agent invented, not researched ones.

## Top 3
1. **[P0] Cookie banner says "no tracking cookies" while a third-party tracker loads and posts a user ID** — both personas named this contradiction as what undid their trust (evaluator, sceptic)
2. **[P1] Pricing page shows no price on any plan — every tier says "Contact sales"** — evaluator gave up at 02:30: "Money, no" (evaluator)
3. **[P1] Privacy page names no partners and contradicts the cookie banner — the sceptic left over it** — she left at 02:40 with her data question unanswered (sceptic)

## The four questions
| Question | Answered? | How long | What they concluded |
|---|---|---|---|
| Is this real? | ✗ | 01:25 (evaluator) | Anonymous testimonials disbelieved; "See it in action" dead; product never shown |
| What does it cost? | ✗ | 02:30 (evaluator, gave up) | "Contact sales" on all three plans; sceptic did not look |
| Who is behind it? | ✓ | 03:50 evaluator · 01:30 sceptic | Named founder, Bristol address, company number — "a real company" |
| What happens to my data? | partly | 05:20 evaluator · 01:05 sceptic | Frankfurt storage on About; privacy page vague and contradicts the banner |

## Objections raised
| Objection | Site's answer | Verdict |
|---|---|---|
| "Nobody has a name. I don't believe these." | Quotes signed "— a happy customer", "— a user", "— anonymous" | made worse |
| "So I can't find out what it costs." | "Pricing depends on your workspace type and sync topology." | made worse |
| "I haven't seen the product and they want my phone number." | Seven-field form, phone `required` | ignored |
| "Which partners? It doesn't say." | "We may share information with partners and service providers" | ignored |
| "The bar said no tracking cookies. This page says they use cookies. One of those is wrong." | Banner "We use no tracking cookies"; tracker POSTs `uid` on load | made worse |
| "I want to see it 'remember' something." | "See it in action" does nothing | ignored |
| Where is my data stored? (sceptic's pre-session question) | "In the EU (Frankfurt) by default." — About only | answered |

## Score
- **Score:** 3/10 — both visitors believed the company exists but neither would trust it with money or data; the cookie and privacy contradiction was decisive.

## Limits on this read
- **Personas:** evaluator (desktop 1440×900), sceptic (iPhone 13) — ⚠ INFERRED (generic)
- **Not reached:** sceptic never opened `/pricing.html`; demo form screenshot blank; app/login not opened
- **Excluded:** none listed in manifest; auth wall always
- **Models:** traversal `fixture-hand-authored` · scoring `opus`
- **Not a compliance review** — findings describe what visitors saw, not legal sufficiency

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| evaluator | not reached | not reached | Fail | Partial |
| sceptic | not reached | not reached | Fail | Fail |

- Q5 outcome — evaluator: "Money, no … Data, unsure." · sceptic: "The About page made them real … The privacy page took it back."
- Price found: 0 of 1 persona who looked · Forms submitted: 0 · Left early: sceptic at 02:50

## Severity flips
- Vague privacy page: **P1 for the sceptic** (she left over it), **P2 for the evaluator** (noted it, stayed, left over price) — split into two findings.
- No visible price: P1 for the evaluator; flip could not be observed — the sceptic never looked for a price.

## Next action
Make the banner match reality (drop or gate the tracker), then name partners on `/privacy.html` and put prices on Starter and Team.
