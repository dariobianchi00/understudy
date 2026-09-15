# Nimbus Notes — trust — Run 2026-09-08 (fixture01)

The About page earns belief in under four minutes and the cookie bar, privacy page and priceless pricing page then take it back, so neither visitor would hand over money or data.

## Top 3
1. **[P0] Cookie bar promises "no tracking cookies" while a third-party analytics beacon fires and the privacy page says cookies are used** — both visitors caught the contradiction and named it as the reason trust collapsed (evaluator, sceptic)
2. **[P1] Pricing page shows no price on any plan; every card ends in "Contact sales"** — the evaluator came for a price, left without one, and will search for a competitor instead (evaluator)
3. **[P1] Privacy page names no partners and no data categories, and routes questions to the demo form** — the sceptic's one question, "who do you share with?", is answered by nothing (evaluator, sceptic)

## Score
- **Score:** 3/10 — two of the four trust questions fail outright, one is answered and then contradicted; only provenance survives.

## The four questions
| Question | Answered? | How long | What they concluded |
|---|---|---|---|
| Is this real? | partly | 03:50 (evaluator) · 01:30 (sceptic) | A real company, yes; a real product, no — anonymous quotes and a demo button that does nothing |
| What does it cost? | ✗ | never (evaluator looked 01:48–02:30; sceptic did not look) | "Without a price I can't take this to my team" |
| Who is behind it? | ✓ | 03:50 (evaluator) · 01:30 (sceptic) | Named founder, Bristol address, company number, eight people — "the first thing that felt real" |
| What happens to my data? | ✗ | never — made worse at 05:20 (evaluator) · 01:05 (sceptic) | Frankfurt is stated on About; then the privacy page and cookie bar contradict each other |

## Objections raised
| Objection | Site's answer | Verdict |
|---|---|---|
| "Nobody has a name. I don't believe these." (evaluator 01:25) | Three quotes signed "— a happy customer", "— a user", "— anonymous" | ignored |
| "So I can't find out what it costs." (evaluator 02:30) | "Pricing depends on your workspace type and sync topology." | made worse |
| "I haven't seen the product and they want my phone number." (evaluator 02:58) | Phone is a required field on the only route from "Contact sales" | ignored |
| "Which partners? It doesn't say." (evaluator 04:50 · sceptic 00:45) | "We may share information with partners and service providers." | ignored |
| "The cookie bar said no tracking. This page says they use cookies. Which is it?" (evaluator 05:20 · sceptic 01:05) | Nothing — the two surfaces simply disagree | made worse |
| "I want to see it 'remember' something." (sceptic 02:20) | "See it in action" — no response on click or tap | made worse |
| "Who is behind this and what happens to my notes" (sceptic pre-session) | About: Priya Raman, Bristol, company no. 14482201, data in Frankfurt | answered |

## Limits on this read
- **Personas:** evaluator (desktop 1440×900), sceptic (iPhone 13) — ⚠ INFERRED (generic)
- **Not reached:** `/features.html` (404 for the evaluator; sceptic never tried) · pricing page and testimonials not seen by the sceptic
- **Excluded:** none in manifest — auth wall always
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | Price found | Price understood | Trust up | Trust down | Q5: money / data |
|---|---|---|---|---|---|
| evaluator | no (looked 01:48–02:30) | no | 2 | 4 | no / unsure |
| sceptic | not looked for | — | 2 | 3 | — / no ("The privacy page took it back") |

## Severity flips
- **"See it in action" does nothing** — P1 for the sceptic (the promise "it remembers everything" had no proof and they left), P2 for the evaluator (noted, then moved on to price). Split as `1b5a8cf51bb4-a` / `-b`.
- Pricing and testimonials were seen only by the evaluator; a flip could not be observed on those.

## Next action
Make the cookie bar tell the truth about the analytics script, or remove the script — until the two agree, every other trust fix is undone on the last page the visitor reads.
