# Nimbus Notes — clarity — Run 2026-09-08 (fixture01)

Neither visitor could say what Nimbus Notes is or who it is for from the site itself — both guessed "notes app" from the brand name and left without ever reaching comprehension.

## Top 3
1. **[P0] Headline never says what Nimbus Notes is — both visitors guessed it from the brand name** — time to comprehension never reached; both left (evaluator, sceptic)
2. **[P2] Plainest explanation of the product is buried in the About FAQ, not on the home page** — the answers exist but are read only after the fold has failed (evaluator, sceptic)
3. **[P2] Landing page never says who Nimbus is for; the only audience lines sit on the pricing page** — a team buyer could not tell if it fits (evaluator, sceptic)

## Score
- **Score:** 3/10 — neither visitor ever understood what the product is or who it serves; both relied on the brand name and left

## Limits on this read
- **Personas:** evaluator (desktop 1440×900), sceptic (iPhone 13) — ⚠ INFERRED (generic); findings rest on invented personas
- **Not reached:** mobile landing page below the fold; mobile `/pricing.html`
- **Excluded:** none in manifest; auth wall (`/app/login.html`) always excluded
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Comprehension
| Persona | What is it? | Who's it for? | What next? | Time to understand |
|---|---|---|---|---|
| evaluator | ✗ (guessed from name) | ✗ | ✗ | never |
| sceptic | ✗ (guessed from name) | ✗ | ✓ (button found; it did nothing) | never |

- Interest died: evaluator at 01:25 on anonymous testimonials; sceptic at 00:30, jumping from the fold straight to the footer.
- Undefined terms quoted: "bi-directional sync graph", "zero-knowledge vault", "workspace type", "sync topology", "card" vs "blocks".

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| evaluator | never | not reached | Fail | Partial |
| sceptic | never | not reached | Fail | Fail |

## Severity flips
- None. Next-step axis differs (evaluator ✗, sceptic ✓), but the dead button is P2 for both.

## Next action
- Rewrite the H1 and subhead to name the product, the job and the audience in plain words, using the About FAQ wording.
