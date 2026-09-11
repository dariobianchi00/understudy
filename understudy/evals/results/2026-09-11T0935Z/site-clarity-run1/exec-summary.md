# Nimbus Notes — clarity — Run 2026-09-08 (fixture01)

Neither visitor ever learned what Nimbus Notes is — both left guessing from the brand name, neither could say who it is for, and the one sentence meant to explain the product, "A bi-directional sync graph with a zero-knowledge vault", was undefinable to both.

## Top 3
1. **[P0] Neither persona could say what the product does; both guessed it from the brand name** — every visitor decision after the fold rested on a guess (evaluator, sceptic)
2. **[P1] The fold's only explanation is two terms neither persona could define** — the sentence carrying the whole value proposition transmits nothing (evaluator, sceptic)
3. **[P1] The home page names no audience, so both personas answered "who is it for" with a guess** — the visitor cannot place themselves, so nothing on the page is aimed at them (evaluator, sceptic)

## Score
- **Score:** 2/10 — both personas finished the visit unable to say what the product is or who it is for; time-to-comprehension was `null` for each.

## Limits on this read
- **Personas:** evaluator (desktop 1440×900), sceptic (iPhone 13) — ⚠ INFERRED (generic `persona_mode`); findings rest on personas the capture invented.
- **Not reached:** `/features.html` (nav link 404s), any logged-in surface.
- **Excluded:** none listed in the manifest; the auth wall is never reported.
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Comprehension
| Persona | What is it? | Who's it for? | What next? | Time to understand |
|---|---|---|---|---|
| evaluator | ✗ | ✗ | ✗ | never |
| sceptic | ✗ | ✗ | ✓ | never |

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| evaluator | never (`time_to_comprehension_seconds: null`) | not reached | Fail | Partial |
| sceptic | never (`time_to_comprehension_seconds: null`) | not reached | Fail | Fail |

- Interest died at 01:25 (evaluator, on the unattributed testimonials) and 00:30 (sceptic, at the fold).
- 8 questions the two visitors could not answer from the site; 0 of them answered above the fold.
- Session lengths: 6.5 min (evaluator), 2.9 min (sceptic, left early).

## Severity flips
- **Next step:** ambiguous for the evaluator (`understood_next_step: false`) and a non-issue for the sceptic (`true`), who never looked for a product action.
- **Fold legibility:** clipped headline and subhead hit the sceptic at 390px only; the evaluator read both in full at 1440px.

## Next action
Rewrite the hero to say what the product is, in the words the About FAQ already uses, and name the audience there.
