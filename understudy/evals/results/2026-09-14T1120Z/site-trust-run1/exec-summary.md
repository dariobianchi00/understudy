# Nimbus Notes — trust — Run 2026-09-14 (fixture01)

Nimbus Notes proved it is a real company and failed every other trust question — both personas left without a price, without knowing who their data is shared with, and with a cookie bar that promised no tracking while an analytics script posted a per-visitor id on the same page load.

## Top 3
1. **[P0] Cookie bar says "no tracking cookies" while the page loads a third-party analytics tracker** — the one claim the site makes about data is contradicted by the same page load; it cost the sceptic the visit (evaluator, sceptic)
2. **[P0] No price on any of three plans, and the only route to a number is a seven-field form** — the evaluator came for a price, gave up at 02:30 and said she would search for an alternative (evaluator)
3. **[P1] Privacy page names none of the partners it says it shares data with** — the sceptic's one question went unanswered and she left at 02:40 (evaluator, sceptic)

## Score
- **Score:** 4/10 — the About page is genuinely convincing, but neither visitor would give money or data after reading the pricing and privacy pages.

## Limits on this read
- **Personas:** evaluator (desktop 1440x900), sceptic (iPhone 13) — ⚠ INFERRED (generic `persona_mode`); findings rest on personas the harness invented, not researched ones.
- **Not reached:** `/features.html` (404), the logged-in app, any product screen.
- **Excluded:** none declared in `manifest.json`; the auth wall is never reported.
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## The four questions
| Question | Answered? | How long | What they concluded |
|---|---|---|---|
| Is this real? | partly | 01:30 (sceptic) / 03:50 (evaluator) | A real company exists; nothing shows the product exists |
| What does it cost? | ✗ | gave up at 02:30 | "So I can't find out what it costs" — three plans, three "Contact sales" |
| Who is behind it? | ✓ | 01:30 | Named founder, Bristol address, company number — the strongest page on the site |
| What happens to my data? | ✗ | never; 01:05 made it worse | Cookie bar and privacy page disagree, and no partner is named |

## Objections raised
| Objection | Site's answer | Verdict |
|---|---|---|
| "The bar said no tracking cookies. This page says they use cookies." | nothing — neither surface acknowledges the other | made worse |
| "'Share with partners' — which partners? Not said." | "We may share information with partners and service providers" | ignored |
| "Every plan says Contact sales. No numbers anywhere." | "Pricing depends on your workspace type and sync topology" | made worse |
| "Three quotes, nobody has a name. I don't believe these." | nothing — no name, company or number attached | ignored |
| "Seven fields. Phone required. I haven't seen the product." | nothing — no explanation of why phone is required | ignored |
| "Clicked 'See it in action' twice. Nothing happened." | nothing — console throws `nimbusBootstrap is not defined` | made worse |
| "Who is behind this and what happens to my notes" (sceptic, pre-session) | About page: founder, address, company number, data in Frankfurt | partly |

## Numbers
| Persona | Session | Price found | Trust up / down | Q5 — money or data? |
|---|---|---|---|---|
| evaluator | 6:30 | ✗ (looked `/pricing.html`, `/index.html#demo`) | 2 / 4 | Money no, data unsure |
| sceptic | 2:54, left early | not attempted | 2 / 3 | About made them real, privacy took it back |

## Severity flips
- **None observable on the evidence that mattered** — both personas read the cookie bar, the privacy page and the About page the same way, up and down.
- **Pricing could not be tested for a flip:** the sceptic never looked ("I didn't look for a price"), so P0 for the evaluator rests on one persona.
- **The testimonials were seen by one persona only** — the sceptic went to the footer at 00:30 and never scrolled the proof section.

## Next action
Make the cookie bar tell the truth about the analytics script, or remove the script — everything else on this list is cheaper to fix and less damaging than a banner the network log contradicts.
