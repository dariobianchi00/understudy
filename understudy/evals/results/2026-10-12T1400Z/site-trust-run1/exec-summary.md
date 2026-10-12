# Nimbus Notes — trust — Run 2026-09-08 (fixture01)

The About page made Nimbus Notes feel like a real company, but neither visitor trusted it with money or data: no price exists, and the cookie bar's "no tracking" claim is contradicted by the privacy page and by a tracker firing on landing.

## Top 3
1. **[P0] Cookie bar says "no tracking cookies" while a third-party tracker loads and posts a user ID** — the site's one data promise is contradicted on page load (evaluator, sceptic)
2. **[P1] Privacy page names no partners and contradicts the cookie bar, so the sceptic left** — the sceptic's whole question went unanswered; session ended at 02:50 (sceptic)
3. **[P1] No price on any plan — every tier says "Contact sales", so the evaluator gave up** — "Money, no"; would search for an alternative (evaluator)

## Score
- **Score:** 3/10 — both visitors believed the company exists, then refused it money (no price) or data (cookie and privacy contradiction)

## Limits on this read
- **Personas:** evaluator, sceptic — ⚠ INFERRED (generic). Findings rest on personas the agent invented, not researched ones.
- **Not reached:** sceptic never looked for pricing; `/features.html` returned 404; the demo-form screenshot (`03-demo-form.png`) is blank, so form evidence is the session log only
- **Excluded:** none in manifest · auth wall always excluded
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## The four questions
| Question | Answered? | How long | What they concluded |
|---|---|---|---|
| Is this real? | partly | 03:50 (evaluator) · 01:30 (sceptic) | Company yes (About page); product no — anonymous quotes, "See it in action" does nothing |
| What does it cost? | ✗ | 02:30 (evaluator gave up) · not attempted (sceptic) | "So I can't find out what it costs. That's the thing I came to check." |
| Who is behind it? | ✓ | 03:50 (evaluator) · 01:30 (sceptic) | Priya Raman, Bristol, 2023, company number 14482201, eight people — "a real company" |
| What happens to my data? | partly | 05:20 (evaluator) · 01:05 (sceptic) | Storage location answered (Frankfurt, on About); partners unnamed; cookie claim contradicted |

## Objections raised
| Objection | Site's answer | Verdict |
|---|---|---|
| "Nobody has a name. I don't believe these." (evaluator) | Nothing — no named customer anywhere on the visited pages | ignored |
| "So I can't find out what it costs." (evaluator) | "Pricing depends on your workspace type and sync topology." | made worse |
| "I haven't seen the product and they want my phone number." (evaluator) | Phone stays required; no alternative route | ignored |
| "With whom? Not said." (sceptic, on partners) | "We may share information with partners and service providers" — no names | ignored |
| "The bar said no tracking cookies. This page says they use cookies. One of those is wrong." (sceptic) | Privacy page: "We use cookies and similar technologies"; tracker fires on landing | made worse |
| "Where is my data stored?" (sceptic's pre-session question) | "In the EU (Frankfurt) by default." — on About, not Privacy | answered |
| "I want to see it 'remember' something." (sceptic) | "See it in action" does nothing when tapped | made worse |

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| evaluator | not reached (comprehension `null`) | not reached — "would not proceed; no price" | Fail | Partial ("Close but off") |
| sceptic | not reached (comprehension `null`) | not reached — "left; data handling unclear" | Fail | Fail ("No") |

- **Q5 outcome:** evaluator — "Money, no… Data, unsure." · sceptic — "The privacy page took it back."
- **trust_up:** About page (both) · FAQ answers (evaluator) · data location (sceptic)
- **trust_down:** 7 distinct items across both personas

## Severity flips
- **Unnamed privacy partners:** P1 for the sceptic (her reason to leave) · P2 for the evaluator (left over price; data only "unsure").
- **No price:** P1 for the evaluator; the sceptic never looked, so a flip could not be observed.

## Next action
- Remove the analytics tracker or change the cookie bar to name it, then rewrite Privacy to name every partner.
