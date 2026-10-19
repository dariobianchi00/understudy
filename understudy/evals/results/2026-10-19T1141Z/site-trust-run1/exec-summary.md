# Nimbus Notes — trust — Run 2026-09-08 (fixture01)

The About page convinced both personas that Nimbus Notes is a real company, but the hidden price, a vague privacy page and a "no tracking cookies" banner that the network log contradicts left neither willing to hand over money or data.

> ⚠ **Personas are INFERRED (generic mode).** These findings rest on personas the agent invented, not on researched users.

## Top 3
1. **[P0] Cookie banner says "no tracking cookies" while every page load sends a visitor ID to a third-party analytics host**: the first promise on the site is false, and both personas caught the contradiction (evaluator, sceptic)
2. **[P1] Privacy page names no partners and commits to nothing specific**: this was the sceptic's whole question, and she left over it (sceptic)
3. **[P1] No price anywhere: all three plans say "Contact sales"**: the evaluator gave up at 02:30, "Money, no" (evaluator)

## The four questions
| Question | Answered? | How long | What they concluded |
|---|---|---|---|
| Is this real? | partly | 03:50 (evaluator) · 01:30 (sceptic) | The company is real (About page). The product is never shown: dead demo button, anonymous quotes |
| What does it cost? | ✗ | 02:30 gave up (evaluator) · not sought (sceptic) | Every plan says "Contact sales"; "I can't find out what it costs" |
| Who is behind it? | ✓ | 03:50 (evaluator) · 01:30 (sceptic) | Named founder, Bristol address, company number: "the first thing … that felt like a real business" |
| What happens to my data? | partly | 01:50 storage found (sceptic) · never resolved | Frankfurt storage is answered. Partners and tracking are not, and the banner and policy disagree |

## Objections raised
| Objection | Site's answer | Verdict |
|---|---|---|
| "Nobody has a name. I don't believe these." | "— a happy customer", "— a user", "— anonymous" | ignored |
| "So I can't find out what it costs." | "Pricing depends on your workspace type and sync topology." | made worse: the explanation was jargon the evaluator couldn't apply |
| "I haven't seen the product and they want my phone number." | Phone is a required field | ignored |
| "Which partners? It doesn't say." | "partners and service providers", none named | ignored |
| "The bar said no tracking cookies. This page says they use cookies." | Network log shows a third-party analytics beacon on landing | made worse |
| "I want to see it 'remember' something." | "See it in action" goes to `#` and does nothing | made worse: a promised demo that fails |
| "who is behind this" (sceptic, pre-session) | About page: Priya Raman, Bristol, 2023, company 14482201 | answered |
| "Where is my data stored?" (sceptic) | "In the EU (Frankfurt) by default." On the About page only | answered (found in an odd place) |

## Score
- **Score:** 3/10 — Both personas believed the company was real, then rejected it: one over no price, the other over a privacy page and banner that disagree.

## Limits on this read
- **Personas:** evaluator, sceptic — ⚠ INFERRED (generic)
- **Not reached:** the sceptic never opened `/pricing.html`; no form submitted; cookie storage not captured; `03-demo-form.png` is blank
- **Excluded:** none in manifest · auth wall (`app/login.html`) never reported
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| evaluator | not reached (left 06:30) | not reached | Fail | Partial |
| sceptic | not reached (left 02:50) | not reached | Fail | Fail |

- Count by severity: **P0 1 · P1 3 · P2 4 · P3 1**
- Q5 outcome: evaluator "Money, no … Data, unsure" · sceptic "The privacy page took it back". Neither would trust them.

## Severity flips
- Privacy page vagueness is **P1 for the sceptic** (she left over it) but **P2 for the evaluator** ("Data, unsure", left over price). See 823356cbe5ec and 4a30d6882dc7.
- No price could not be compared across personas. The sceptic never looked, so a flip could not be observed.

## Next action
- Make the cookie banner true, then publish one real price and name the privacy-page partners. All three are copy or config changes.
