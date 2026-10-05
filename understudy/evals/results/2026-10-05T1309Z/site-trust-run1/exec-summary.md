# Nimbus Notes — trust — Run 2026-09-08 (fixture01)

The About page convinced both visitors a real company is behind Nimbus, but a "no tracking cookies" bar contradicted by its own tracker, an unnamed-partners privacy page and prices hidden behind "Contact sales" left neither willing to trust it with money or data.

## Top 3
1. **[P0] Cookie banner says "no tracking cookies" while every visit sends a visitor ID to a third-party tracker** — both personas caught the contradiction; it erased the trust About had built (evaluator, sceptic)
2. **[P1] No plan shows a price, so the evaluator could not learn the cost and gave up** — "Money, no"; would search for an alternative (evaluator)
3. **[P1] Privacy page names no partners, and the sceptic left because of it** — her stated leave condition, met at 00:45 (sceptic)

> ⚠ **Personas are INFERRED (`persona_mode: generic`).** Findings rest on personas the agent invented, not researched buyers.

## The four questions
| Question | Answered? | How long | What they concluded |
|---|---|---|---|
| Is this real? | partly | 03:50 (evaluator) · 01:30 (sceptic) | Company real via About; product never shown, testimonials disbelieved |
| What does it cost? | ✗ | gave up 02:30 (evaluator) · not asked (sceptic) | Every plan "Contact sales"; no number anywhere |
| Who is behind it? | ✓ | 03:50 (evaluator) · 01:30 (sceptic) | Priya Raman, Bristol, 2023, company number — "a real company" |
| What happens to my data? | partly | 05:20 (evaluator) · 01:50 (sceptic) | Frankfurt storage found on About; partners unnamed; cookie bar contradicted |

## Objections raised
| Objection | Site's answer | Verdict |
|---|---|---|
| "no price, or a page that is all adjectives" (evaluator) | "Contact sales" ×3; "Pricing depends on your workspace type and sync topology." | made worse |
| "Nobody has a name. I don't believe these." (evaluator) | Nothing — no named customer anywhere | ignored |
| "I haven't seen the product and they want my phone number." (evaluator) | Phone stays required | ignored |
| "Which partners? It doesn't say." (both) | "We may share information with partners and service providers" | ignored |
| "The cookie bar said no tracking. This page says they use cookies… Which is it?" (both) | Banner "no tracking cookies"; network shows tracker `collect?uid=…` | made worse |
| "who is behind this" (sceptic, pre-session) | About: founder, address, company number | answered |
| "a privacy page that is a link to a generic policy" (sceptic leave condition) | Four-sentence generic policy | made worse |
| "I want to see it 'remember' something." (sceptic) | "See it in action" does nothing | ignored |

## Score
- **Score:** 3/10 — both visitors believed the company exists, then neither would trust it with money or data; one left over privacy.

## Limits on this read
- **Personas:** evaluator (desktop), sceptic (iPhone 13) — ⚠ INFERRED (generic)
- **Not reached:** terms page; sceptic never opened Pricing or the demo form; cookie storage not captured
- **Excluded:** none in manifest · auth wall always
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| evaluator | not reached (comprehension null) | not reached | Fail | Partial |
| sceptic | not reached (comprehension null) | not reached | Fail | Fail |

- Q5 outcome: evaluator — money no, data unsure · sceptic — About made them real, "The privacy page took it back."
- `trust_up`: 2 + 2, all from About · `trust_down`: 4 + 3
- Findings: P0 ×1 · P1 ×2 · P2 ×5 · P3 ×2

## Severity flips
- Unnamed privacy partners: **P1 for the sceptic** (she left) · **P2 for the evaluator** (noted, left over price instead)
- Missing price: P1 for the evaluator; flip not observable — the sceptic never looked

## Next action
- Make the cookie banner true — remove the tracker or disclose it with a real choice — then name partners on `/privacy`.
