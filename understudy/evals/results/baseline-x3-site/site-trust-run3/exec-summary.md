# Nimbus Notes — trust — Run 2026-09-08 (fixture01)

Both visitors believed the company exists and neither believed what it says about their data, because the cookie bar promises "no tracking cookies" while a third-party tracker fires on landing and the privacy page admits cookies and unnamed "partners".

## Top 3
1. **[P0] Cookie bar says no tracking cookies while a third-party tracker fires and the privacy page says cookies are used** — the one trust gain (About page) was undone on the next click; sceptic left on it (evaluator, sceptic)
2. **[P1] No plan shows a price; all three say Contact sales and the footnote adds an unknown** — evaluator gave up at 02:30 and "would search for an alternative" (evaluator)
3. **[P1] Privacy page names no partners, no data types, and routes questions to the demo form** — sceptic's verdict: "left; data handling unclear" (sceptic; P2 for evaluator)

## Score
- **Score:** 3/10 — a real company behind a site that contradicts itself on tracking and shows no price, no named customer, and no product.

## The four questions
| Question | Answered? | How long | What they concluded |
|---|---|---|---|
| Is this real? | partly | 03:50 (evaluator) · 01:30 (sceptic) | Real company, yes; real product, never seen — "See it in action" does nothing, quotes are anonymous |
| What does it cost? | ✗ | gave up 02:30 (evaluator) · not asked (sceptic) | "Contact sales" ×3; "Pricing depends on your workspace type and sync topology" |
| Who is behind it? | ✓ | 03:50 (evaluator) · 01:30 (sceptic) | Nimbus Notes Ltd, Priya Raman, Bristol, company number — "first thing that felt real" |
| What happens to my data? | ✗ | 05:20 (evaluator) · 01:05 (sceptic) | Banner and privacy page disagree; partners unnamed; Frankfurt answer found only on About |

## Objections raised
| Objection | Site's answer | Verdict |
|---|---|---|
| "The cookie bar said no tracking. This page says they use cookies and share with partners. Which is it?" | Nothing — and the network log shows a tracker POST on landing | made worse |
| "'Share with partners' — which partners? Not said." | Nothing | ignored |
| "Nobody has a name. I don't believe these." | Nothing | ignored |
| "I don't know what my workspace type is. I haven't got one." | Nothing — the footnote introduces the term without defining it | made worse |
| "I haven't seen the product and they want my phone number." | Nothing | ignored |
| "I want to see it 'remember' something. The button does nothing when I tap it." | Nothing — the only demonstration link is dead | made worse |
| "Where is my data stored?" | Answered on About: "In the EU (Frankfurt) by default" | answered |

## Limits on this read
- **Personas:** evaluator (desktop 1440×900), sceptic (iPhone 13) — ⚠ INFERRED (generic)
- **Not reached:** sceptic never opened Pricing or read testimonials; evaluator's demo-form screenshot (`03-demo-form.png`) is blank, form contents rest on `session.log:21`
- **Excluded:** none in manifest — auth wall always
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | Session | Price found | Trust up | Trust down | Q5 — trust with money / data |
|---|---|---|---|---|---|
| evaluator | 06:30 | no (gave up 02:30) | 2 | 4 | money: no · data: unsure |
| sceptic | 02:50 (left early) | not attempted | 2 | 3 | data: About gave it, "the privacy page took it back" |

## Severity flips
- **Privacy page vagueness** — P1 for the sceptic (it is why they left); P2 for the evaluator (nicked trust, but price drove the exit). Split as `69aaf3f1d3ab-a` / `-b`.
- **Pricing** — P1 for the evaluator; the sceptic never looked, so a flip could not be observed.
- **Anonymous testimonials** — P2 for the evaluator; the sceptic skipped straight to the footer, so a flip could not be observed.

## Next action
- Make the cookie bar tell the truth: remove the tracker or rewrite the banner, and name the partners on `/privacy.html` — nothing else on the site can be believed until the two agree.
