# Nimbus Notes — trust — Run 2026-09-21 (fixture01)

Both visitors decided the company was real and still refused it, because the cookie bar, the privacy page and the network log tell three different stories about what happens to their data — and neither could find a price.

## Top 3
1. **[P0] Cookie bar's no-tracking claim is contradicted by the privacy page and by the network log** — the one hard claim the site makes about data is visibly untrue on the same page load; both personas named it as the reason they stopped. (evaluator, sceptic)
2. **[P1] Privacy page names no partners, and the sceptic left the site over it** — cost the whole visit at 02:40, 30 seconds after the About page had won her over. (sceptic)
3. **[P1] Every pricing plan says Contact sales, and the reason given is unusable** — the evaluator's only question, unanswerable in 42 seconds of looking; he left to find a competitor with a number on the page. (evaluator)

## Score
- **Score:** 3/10 — both visitors reached a verdict and rejected it: one would not pay because no price exists, the other would not hand over data because the site contradicts itself about tracking.

## Limits on this read
- **Personas:** evaluator (desktop-1440x900), sceptic (iphone-13) — ⚠ INFERRED (generic `persona_mode`); findings rest on personas the run invented, not researched ones.
- **Not reached:** `/features.html` (404) · no form submitted · logged-in app never seen.
- **Excluded:** none declared in `manifest.json`; auth wall never reported.
- **Models:** traversal `fixture-hand-authored` · scoring `opus`
- **Scope:** everything below is what the personas could verify on the site. Nothing here is a claim about the company, and no compliance judgement is made or implied.

## The four questions
| Question | Answered? | How long | What they concluded |
|---|---|---|---|
| Is this real? | partly | 01:30 sceptic · 03:50 evaluator | The About page settled it; the home page's own proof section reduced trust. |
| What does it cost? | ✗ | never — evaluator looked 01:48–02:30 | "So I can't find out what it costs. That's the thing I came to check." |
| Who is behind it? | ✓ | 01:30 sceptic · 03:50 evaluator | Named founder, Bristol address, company number 14482201, eight people. |
| What happens to my data? | ✗ | never — read at 00:45 sceptic · 04:50 evaluator | Two on-site statements disagree; partners unnamed. |

## Objections raised
| Objection | Site's answer | Verdict |
|---|---|---|
| "The bar said no tracking cookies. This page says they use cookies. One of those is wrong." | Nothing reconciles them; the landing load also fetches a third-party tracker. | made worse |
| "'Share with partners' — which partners? Not said." | "We may share information with partners and service providers to improve your experience." | ignored |
| "Every plan says Contact sales. No numbers anywhere." | "Pricing depends on your workspace type and sync topology." | made worse |
| "Three quotes, nobody has a name. I don't believe these." | The quotes are signed "— a happy customer", "— a user", "— anonymous". | made worse |
| "I haven't seen the product and they want my phone number." | Nothing; phone is a required field. | ignored |
| "Who is behind this and what happens to my notes" (sceptic, pre-session) | About page: founder, address, company number, data in Frankfurt. | partly |

## Numbers
| Persona | Price found | Provenance found | Data question answered | Q5 — money / data |
|---|---|---|---|---|
| evaluator | ✗ (looked 01:48–02:30) | ✓ 03:50 | ✗ | no / unsure |
| sceptic | not sought | ✓ 01:30 | ✗ | not stated / taken back |

## Severity flips
- **The privacy page flips.** Sceptic: session-ending at 02:40 (P1). Evaluator: same page, same objection, read at 04:50, carried on to the end and rated data "unsure" (P2). Split into two findings, never averaged.
- The sceptic left at 2.9 minutes and never opened pricing; the evaluator left at 6.5 minutes and never opened a form beyond looking. Neither persona's worst finding was the other's.

## Next action
Make the cookie bar match the network log, then name the partners on `/privacy.html` — those two edits address the only objection both personas raised.
