# Nimbus Notes — clarity — Run 2026-09-08 (fixture01)

Neither visitor ever learned what Nimbus Notes is from the site — both guessed "notes app" from the name, nobody could say who it is for, and the one button that promised to show the product does nothing.

## Comprehension
| Persona | What is it? | Who's it for? | What next? | Time to understand |
|---|---|---|---|---|
| evaluator (desktop 1440×900) | partly — guessed from the name | ✗ | ✗ | never |
| sceptic (iPhone 13) | partly — guessed from the name and a friend | ✗ | partly — saw the button; it did nothing | never |

## Top 3
1. **[P1] Landing fold never says what the product is** — both personas left with a guess, not an answer; `time_to_comprehension_seconds: null` twice (evaluator, sceptic)
2. **[P1] The only "See it in action" button goes nowhere** — the one path to seeing what the product does is dead; both personas clicked it and left without seeing anything (evaluator, sceptic)
3. **[P2] Hero subhead is jargon the visitor cannot parse** — "bi-directional sync graph", "zero-knowledge vault" were both flagged as unknown inside 18 seconds (evaluator)

## Score
- **Score:** 3/10 — two personas, two `null` comprehension times; the site's clearest sentences live on About, and the hero's only button is dead.

## Limits on this read
- **Personas:** evaluator, sceptic — ⚠ INFERRED (generic)
- **Not reached:** `/features.html` (404 on both attempts); `01-scrolled.png` captured blank, so below-fold sections are read from `session.log` only
- **Excluded:** none — auth wall never reported
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| evaluator | never | not reached | Fail | Partial — "close but off" |
| sceptic | never | not reached | Fail | Fail — "No" |

- TTFV here is time-to-comprehension; both `timeline.json` values are `null`.
- Evaluator lost interest at 01:25 on the anonymous "Loved by teams" quotes; sceptic at 00:30, before scrolling.
- Terms neither persona could define, verbatim: "bi-directional sync graph", "zero-knowledge vault", "workspace type", "sync topology".
- Evaluator's Q4 list has 5 unanswered questions; 2 of them are definitions of on-page words.

## Severity flips
None — both personas failed all three comprehension axes the same way; the sceptic's shorter visit changed nothing.

## Next action
Rewrite the hero to say in plain words what Nimbus Notes is and who it is for, and make "See it in action" open something.
