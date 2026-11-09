# Nimbus Notes — trust — Run 2026-09-08 (fixture01)

Neither persona would trust Nimbus Notes with money or data, because a cookie bar contradicted by the site's own traffic and a price-free pricing page undid the credibility the About page earned.

## Top 3
1. **[P0] Cookie bar says no tracking cookies while a third-party analytics script posts a visitor ID on load** — the first data promise is false on its face; the sceptic left (evaluator, sceptic)
2. **[P1] Pricing page shows no price on any plan** — the evaluator's one question went unanswered; would search for an alternative (evaluator)
3. **[P1] Privacy page names no partners** — the sceptic came to learn what happens to their notes and left without an answer (sceptic; P2 for evaluator)

## The four questions
| Question | Answered? | How long | What they concluded |
|---|---|---|---|
| Is this real? | partly | 03:50 (evaluator) · 01:30 (sceptic) | Company felt real via About; testimonials disbelieved, product never shown |
| What does it cost? | ✗ | gave up 02:30 (evaluator); sceptic did not look | "So I can't find out what it costs." |
| Who is behind it? | ✓ | 03:50 (evaluator) · 01:30 (sceptic) | Named founder, Bristol address, company number — "a real company" |
| What happens to my data? | partly | 04:20 (evaluator) · 01:50 (sceptic) | Frankfurt storage found on About; privacy page and cookie bar contradict — "Data, unsure" |

## Objections raised
| Objection | Site's answer | Verdict |
|---|---|---|
| "So I can't find out what it costs." | "Pricing depends on your workspace type and sync topology." | made worse |
| "I haven't seen the product and they want my phone number." | Phone stays required | ignored |
| "Nobody has a name. I don't believe these." | Quotes attributed to "a happy customer", "a user", "anonymous" | made worse |
| "With whom? Not said." | "We may share information with partners and service providers" | ignored |
| "The bar said no tracking cookies. This page says they use cookies." | Banner "no tracking cookies"; network shows third-party analytics `collect?uid=` | made worse |
| "Where is my data stored?" | "In the EU (Frankfurt) by default." — on About only | answered |
| "I want to see it 'remember' something." | "See it in action" does nothing | ignored |

## Score
- **Score:** 3/10 — both visitors believed the company exists, then left distrusting its data claims; one could not find a price

## Limits on this read
- **Personas:** evaluator, sceptic — ⚠ INFERRED (generic); findings rest on personas the agent invented
- **Not reached:** log-in/app; sceptic never opened Pricing or the testimonials
- **Excluded:** none in manifest; auth wall always
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | Q5 money | Q5 data | trust_up | trust_down | Price found | Outcome |
|---|---|---|---|---|---|---|
| evaluator | no | unsure | 2 | 4 | no | would not proceed (06:30) |
| sceptic | — | no | 2 | 3 | not sought | left early (02:50) |

- Findings: P0 1 · P1 3 · P2 4 · P3 1

## Severity flips
- Privacy page naming no partners: P1 for the sceptic (left over it), P2 for the evaluator (price decided that exit)

## Next action
- Make the cookie bar match the network traffic, then publish a price.
