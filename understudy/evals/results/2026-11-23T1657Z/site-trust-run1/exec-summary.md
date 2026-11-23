# Nimbus Notes — trust — Run 2026-09-08 (fixture01)

The About page convinced both visitors Nimbus is a real company, but a "no tracking cookies" banner contradicted by a live analytics tracker, a partner-less privacy page and no price undid it — neither would trust them with money, and the sceptic left over data.

## Top 3
1. **[P0] Cookie bar claims no tracking while a third-party analytics tracker sends a user ID on page load** — the site's first data claim is false on its own traffic (evaluator, sceptic)
2. **[P1] Privacy page names no partners and contradicts the cookie bar — the sceptic left over it** — the visit ended at 02:40 on this page (sceptic)
3. **[P1] No plan shows a price, so the evaluator gave up on cost and would not trust them with money** — "Money, no"; would search for an alternative (evaluator)

## The four questions
| Question | Answered? | How long | What they concluded |
|---|---|---|---|
| Is this real? | partly | 03:50 (evaluator) · 01:30 (sceptic) | Company is real via About; product never shown, testimonials anonymous |
| What does it cost? | ✗ | 01:48–02:30, gave up (evaluator) | "Contact sales" on all three plans; no number anywhere |
| Who is behind it? | ✓ | 03:50 (evaluator) · 01:30 (sceptic) | Named founder, Bristol address, company number — "a real company" |
| What happens to my data? | partly | 01:50 (sceptic, Frankfurt) | Location found on About; partners unnamed, cookie claims contradict |

## Objections raised
| Objection | Site's answer | Verdict |
|---|---|---|
| "So I can't find out what it costs." | "Pricing depends on your workspace type and sync topology." | made worse |
| "I haven't seen the product and they want my phone number." | Required phone field on the only route to a price | made worse |
| "Nobody has a name. I don't believe these." | Nothing — no named customer anywhere visited | ignored |
| "'Share with partners' — which partners? Not said." | "We may share information with partners and service providers" | ignored |
| "The bar said no tracking cookies. This page says they use cookies. One of those is wrong." | Banner says none; network shows a third-party tracker with a `uid` | made worse |
| "who is behind this" (sceptic's pre-session question) | Founder, address, company number on About | answered |
| "I want to see it 'remember' something." | "See it in action" does nothing | ignored |

## Score
- **Score:** 3/10 — both visitors believed the company existed, then rejected it on data and price; one left, neither would pay

## Limits on this read
- **Personas:** evaluator (desktop), sceptic (iPhone 13) — ⚠ INFERRED (generic); findings rest on personas the agent invented
- **Not reached:** sceptic never opened Pricing; no terms page; no cookie jar captured
- **Excluded:** none in manifest · auth wall always excluded
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| evaluator | not reached (comprehension null; left 06:30) | not reached | Fail | Partial |
| sceptic | not reached (comprehension null; left 02:50) | not reached | Fail | Fail |

## Severity flips
- Privacy page vagueness + cookie contradiction: **P1 for the sceptic** (left over it) vs **P2 for the evaluator** (data "unsure", left over price) — split into two findings.
- Pricing: sceptic never looked, so a flip could not be observed.

## Next action
- Make the cookie banner tell the truth about the analytics tracker, then name every third party on /privacy.html.
