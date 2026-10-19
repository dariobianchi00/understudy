# Nimbus Notes — clarity — Run 2026-09-08 (fixture01)

Neither visitor could tell from the page what Nimbus Notes is or who it is for; both guessed "notes app" from the brand name and never reached real comprehension.

> ⚠ **Personas are INFERRED (generic mode).** Findings rest on invented personas, not researched ones; weigh them accordingly.

## Top 3
1. **[P0] Neither persona could say what Nimbus Notes is from the page; comprehension never reached** — "Your thoughts, everywhere." names no task; time to comprehension is `null` for both (evaluator, sceptic)
2. **[P1] Evaluator could not tell whether the product is for individuals or teams** — he came to judge a team replacement and left without an answer (evaluator)
3. **[P2] Clearest product explanation sits on the About page, not the landing page** — the plain offline-sync, export and Frankfurt answers are two clicks from where visitors judge (evaluator, sceptic)

## Score
- **Score:** 3/10 — neither visitor ever understood what the product does from the page; both relied on the brand name to guess

## Limits on this read
- **Personas:** evaluator (desktop 1440×900), sceptic (iPhone 13, 390×844) — ⚠ INFERRED (generic)
- **Not reached:** `/features.html` (404); sceptic never scrolled the landing page
- **Excluded:** none in manifest · auth wall (`/app/login.html`) always excluded
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Comprehension
| Persona | What is it? | Who's it for? | What next? | Time to understand |
|---|---|---|---|---|
| evaluator | ✗ | ✗ | ✗ | never |
| sceptic | ✗ | ✗ | ✓ | never |

- "What" marked ✗ for both: answers came from the logo word "Notes", not the page (`guessed: true`)
- Point of lost interest: evaluator 01:25 on "Loved by teams" testimonials; sceptic 00:30, after the fold only

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| evaluator | never | not reached | Fail | Partial ("close but off") |
| sceptic | never | not reached | Fail | Fail ("No") |

- Severity count: P0 ×1 · P1 ×1 · P2 ×7 · P3 ×1
- Undefined terms quoted: "bi-directional sync graph", "zero-knowledge vault", "workspace type", "sync topology", "card" vs "blocks"

## Severity flips
- Not knowing who the product is for: P1 for evaluator (blocked his team-fit question) · P2 for sceptic (not her question)

## Next action
- Rewrite the hero H1 and subhead to say, in plain words, what it does and for whom; lift the About FAQ answers onto the landing page.
