# Nimbus Notes — clarity — Run 2026-09-08 (fixture01)

Two of two visitors left unable to say what Nimbus Notes does or who it is for — time-to-comprehension was never in both sessions — because the only words on the landing page that name the category are the brand name and an anonymous testimonial.

## Top 3
1. **[P0] Neither persona could say what the product does; the landing page never names the category** — both visitors guessed the category from the wordmark and one left in 2:50 (evaluator, sceptic)
2. **[P1] The plainest description of the product is on the About page, two clicks from the fold** — the sentence that would have fixed comprehension is already written and sits where nobody lands (evaluator, sceptic)
3. **[P1] The nav item that promises an explanation of the product returns a 404** — `Features` is the one destination named for explaining the product and has no page behind it (evaluator)

## Score
- **Score:** 2/10 — the lens's only question was answered "no" by both personas: neither could state what the product is or who it is for, at any point in the session.

## Comprehension
| Persona | What is it? | Who's it for? | What next? | Time to understand |
|---|---|---|---|---|
| evaluator | ✗ | ✗ | ✗ | never |
| sceptic | ✗ | ✗ | ✓ | never |

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| evaluator | never (6:30 session) | not reached | Fail | Partial — "close but off" |
| sceptic | never (2:50 session) | not reached | Fail | Fail — "No" |

- Unanswered questions carried to the debrief: 5 (evaluator), 3 (sceptic)
- Undefinable terms quoted by personas: 4 — "bi-directional sync graph", "zero-knowledge vault", "workspace type", "sync topology"
- Interest died at 01:25 (evaluator, anonymous testimonials) and 00:30 (sceptic, the fold itself)
- Pages that would explain the product: 1 of 2 reachable — `/features.html` is a 404

## Limits on this read
- **Personas:** evaluator (desktop 1440×900), sceptic (iPhone 13, 390×844) — **⚠ INFERRED (generic)**; findings rest on personas the agent invented, not researched ones
- **Not reached:** `/features.html` (404), anything behind `Log in`, viewports between 390px and 1440px
- **Excluded:** none declared in `manifest.json`; the auth wall is never reported
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Severity flips
- **The next-step axis flipped:** the evaluator could not tell what the page wanted (`understood_next_step: false`) while the sceptic could (`true`) — the desktop fold puts the outlined CTA at the bottom of a 900px viewport, the phone puts it directly under the headline.
- **The fold itself flipped by device:** readable at 1440px, clipped off the right edge at 390px, where the whole explanatory subhead is unreachable — reported as its own finding.

## Next action
Put the About page's plain-language answer in the hero, name the audience beside it, and re-test the fold at 390px.
