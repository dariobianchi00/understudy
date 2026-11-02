# Nimbus Notes — trust — Run 2026-09-08 (fixture01)

Both visitors believed the company was real but trusted it with neither money nor data, because no price is shown and the cookie bar contradicts the privacy page.

> **⚠ Personas are INFERRED (`persona_mode: generic`).** Findings rest on visitors the agent invented, not researched ones.

## Top 3
1. **[P0] Cookie bar says no tracking while the privacy page says cookies and a third-party analytics call fires** — undid the trust the About page earned; sceptic left over it (evaluator, sceptic)
2. **[P1] Privacy page names no partners, so the sceptic left without knowing who gets her notes** — her one question went unanswered; exit at 02:40 (sceptic)
3. **[P1] No price on the pricing page; every plan says "Contact sales"** — "Money, no"; evaluator would not proceed (evaluator)

## Score
- **Score:** 3/10 — both visitors believed the company existed, yet one would not pay and the other left over unclear data handling.

## The four questions
| Question | Answered? | How long | What they concluded |
|---|---|---|---|
| Is this real? | partly | 03:50 (evaluator) · 01:30 (sceptic) | Company real via About; product never shown, testimonials disbelieved |
| What does it cost? | ✗ | gave up 02:30 (evaluator) · not sought (sceptic) | "Every plan says Contact sales. No numbers anywhere." |
| Who is behind it? | ✓ | 03:50 (evaluator) · 01:30 (sceptic) | Named founder, Bristol address, company number — "a real company" |
| What happens to my data? | partly | 01:50 (sceptic, location) · never (sharing, tracking) | Frankfurt storage found on About; partners and tracking unresolved |

## Objections raised
| Objection | Site's answer | Verdict |
|---|---|---|
| "Three quotes, nobody has a name. I don't believe these." | Attributions "— a happy customer", "— a user", "— anonymous" | made worse |
| "Every plan says Contact sales. No numbers anywhere." | "Pricing depends on your workspace type and sync topology." | made worse |
| "Seven fields. Phone required. I haven't seen the product and they want my phone number." | Nothing; phone field stays required | ignored |
| "'Share with partners' — which partners? Not said." | Nothing on any page visited | ignored |
| "The bar said no tracking cookies. This page says they use cookies." | Privacy page: "We use cookies and similar technologies." | made worse |
| "Where is my data stored?" (sceptic's question) | About FAQ: "In the EU (Frankfurt) by default." | answered |
| "I want to see it 'remember' something." | "See it in action" does nothing | ignored |

## Limits on this read
- **Personas:** evaluator (desktop), sceptic (iPhone 13) — ⚠ INFERRED (generic)
- **Not reached:** terms page; sceptic never opened Pricing; demo-form screenshot captured blank
- **Excluded:** none in manifest; auth wall always excluded
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| evaluator | never (comprehension null) | not reached | Fail | Partial |
| sceptic | never (comprehension null) | not reached | Fail | Fail |

- Trust up: evaluator 2 · sceptic 2 — all from the About page.
- Trust down: evaluator 4 · sceptic 3.
- Q5 outcome: evaluator "Money, no … Data, unsure" · sceptic "The privacy page took it back."

## Severity flips
- Privacy page naming no partners: **P1 for the sceptic** (she left over it) · **P2 for the evaluator** (noted, left over price instead).
- Missing price: could not be tested for a flip — the sceptic never looked.

## Next action
- Make the cookie bar, privacy page and analytics tag say the same thing, then put a price on Starter and Team.
