# Nimbus Notes — clarity — Run 2026-09-08 (fixture01)

Neither visitor could say what Nimbus Notes is from the page; both left guessing "a notes app" from the brand name, never from the headline.

> ⚠ **Generic personas.** Both personas were INFERRED, not researched; every finding rests on invented visitors.

## Top 3
1. **[P1] Neither visitor could say what Nimbus Notes is from the page; both guessed it from the brand name** — time to comprehension is `null` for both; "Your thoughts, everywhere." names no product (evaluator, sceptic)
2. **[P2] The hero subhead uses jargon the visitor could not define** — "bi-directional sync graph" and "zero-knowledge vault" turned the only explanatory line into noise (evaluator)
3. **[P2] The clearest description of what Nimbus does is in the About page FAQ, not on the home page** — offline, Markdown export and Frankfurt storage sit two clicks from where visitors judged it (evaluator, sceptic)

## Score
- **Score:** 3/10 — neither visitor learned from the site what it is or who it is for; both left guessing from the name

## Limits on this read
- **Personas:** evaluator (desktop 1440×900), sceptic (iPhone 13, 390×844) — ⚠ INFERRED (generic)
- **Not reached:** sceptic never scrolled the home page body or opened Pricing; `/features.html` returns 404
- **Excluded:** none in manifest · auth wall (`/app/login.html`) always excluded
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Comprehension
| Persona | What is it? | Who's it for? | What next? | Time to understand |
|---|---|---|---|---|
| evaluator | partly (guessed from name) | ✗ | ✗ | never |
| sceptic | partly (guessed from name and a friend) | ✗ | partly (button found; it does nothing) | never |

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| evaluator | never | not reached | Fail | Partial |
| sceptic | never | not reached | Fail | Fail |

- Point of lost interest: evaluator 01:25 on the anonymous "Loved by teams" quotes; sceptic 00:30, straight from the fold to the footer
- Undefined terms quoted: "bi-directional sync graph", "zero-knowledge vault", "workspace type", "sync topology", "vault residency", "card" vs "blocks"
- Findings by severity: P0 0 · P1 1 · P2 9 · P3 2

## Severity flips
- None — both personas failed the "what" and "who" axes the same way; next step differed (evaluator ✗, sceptic partly) without a severity change.

## Next action
- Rewrite the H1 and subhead in plain words naming the product, its job and its audience, then move the About FAQ answers under the hero.
