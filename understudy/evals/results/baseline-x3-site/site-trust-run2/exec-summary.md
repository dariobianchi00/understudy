# Nimbus Notes — trust — Run 2026-09-08 (fixture01)

Both visitors found a real company on the About page and then lost it again, because the cookie bar contradicts the privacy page and no plan has a price.

## Top 3
1. **[P0] Cookie bar says no tracking cookies while a third-party tracker loads and the privacy page says cookies are used** — the one contradiction both personas caught unprompted; it reversed the About-page gain and was the sceptic's exit reason (evaluator, sceptic)
2. **[P1] No plan shows a price; every card says Contact sales and the footnote adds jargon instead of a reason** — the evaluator came for a price, gave up at 02:30, answered "Money, no" (evaluator)
3. **[P1] Privacy page names no partners the site shares data with** — "partners and service providers" was the whole answer to the sceptic's only question; she left at 02:40 (sceptic; P2 for evaluator)

## The four questions
| Question | Answered? | How long | What they concluded |
|---|---|---|---|
| Is this real? | partly | 03:50 (evaluator) · 01:30 (sceptic) | The company is real (About); the product never appears — dead "See it in action", anonymous quotes, no screenshot |
| What does it cost? | ✗ | gave up 02:30 (evaluator) · not looked (sceptic) | "Contact sales" ×3 and "depends on your workspace type and sync topology" — no number anywhere |
| Who is behind it? | ✓ | 03:50 (evaluator) · 01:30 (sceptic) | Nimbus Notes Ltd, eight people, Priya Raman, Bristol address, company number — believed by both |
| What happens to my data? | ✗ | 05:20 (evaluator) · 01:05 (sceptic) | Frankfurt storage (on About) believed; cookie bar vs privacy page contradiction and unnamed "partners" left both unsure |

## Objections raised
| Objection | Site's answer | Verdict |
|---|---|---|
| "Every one says 'Contact sales'. No numbers anywhere." | "Pricing depends on your workspace type and sync topology." | made worse |
| "The cookie bar said no tracking. This page says they use cookies and share with partners. Which is it?" | Nothing — and the network log shows a third-party tracker posting a uid on load | made worse |
| "'We may share information with partners and service providers.' Which partners?" | Nothing | ignored |
| "Nobody has a name. I don't believe these." | Nothing — three quotes signed "a happy customer", "a user", "anonymous" | ignored |
| "I haven't seen the product and they want my phone number." | Nothing — phone stays required | ignored |
| "I want to see it 'remember' something. The button does nothing when I tap it." | Nothing | ignored |
| "who is behind this and what happens to my notes" (sceptic, pre-session) | About: named founder, address, company number, "In the EU (Frankfurt) by default" | partly — who: answered; data: contradicted on Privacy |

## Score
- **Score:** 3/10 — Neither visitor would hand over money, and neither could say what happens to their data; the About page is the only surface either believed.

## Limits on this read
- **Personas:** evaluator (desktop 1440×900), sceptic (iPhone 13) — ⚠ INFERRED (generic); findings rest on personas the run invented, not researched ones
- **Not reached:** sceptic never opened `/pricing.html` or the demo form; no terms page exists; `03-demo-form.png` captured blank
- **Excluded:** none in manifest — auth wall always
- **Models:** traversal `fixture-hand-authored` · scoring `opus`
- **Not a compliance review** — nothing here says whether any policy is legally sufficient; every finding is what the site says or does not say

## Numbers
| Persona | Session | Price found | Q5 money | Q5 data | Trust up | Trust down | Left early |
|---|---|---|---|---|---|---|---|
| evaluator | 06:30 | no (gave up 02:30) | "no" | "unsure" | 2 | 4 | no |
| sceptic | 02:50 | not looked | — | contradicted, left | 2 | 3 | yes |

## Severity flips
- **Privacy page names no partners** — P1 for the sceptic (her exit reason) · P2 for the evaluator (a nick; price was the exit). Split as `472ead18f72a-a` / `-b`.
- **No price** — P1 for the evaluator · not observed for the sceptic, who never looked; a flip cannot be claimed.

## Next action
Make the cookie bar and `/privacy.html` tell the same story (name the analytics provider and the partners, or remove the tracker), then put a number on the Starter plan.
